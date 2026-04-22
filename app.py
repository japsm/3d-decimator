from flask import Flask, request, render_template, send_file, jsonify, send_from_directory
import trimesh
import numpy as np
import os
from pathlib import Path
import zipfile
from datetime import datetime, timedelta
import json
import shutil

app = Flask(__name__)

# Configuration - use persistent storage
UPLOAD_FOLDER = '/app/uploads'
OUTPUT_FOLDER = '/app/outputs'
CONVERSIONS_FILE = '/app/conversions.json'
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB per file
MAX_FILES = 20
RETENTION_DAYS = 5

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

REDUCTION_LEVELS = {
    'light': 0.75,
    'medium': 0.50,
    'heavy': 0.25
}

SUPPORTED_FORMATS = ['stl', 'obj', '3mf']

def cleanup_old_files():
    """Delete files older than RETENTION_DAYS"""
    cutoff_time = datetime.now() - timedelta(days=RETENTION_DAYS)
    
    for filename in os.listdir(OUTPUT_FOLDER):
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.isfile(filepath):
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_time < cutoff_time:
                try:
                    os.remove(filepath)
                except Exception:
                    pass

def load_conversions():
    """Load conversion history from JSON file"""
    if os.path.exists(CONVERSIONS_FILE):
        try:
            with open(CONVERSIONS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_conversion(conversion_data):
    """Save a conversion record"""
    conversions = load_conversions()
    conversions.append(conversion_data)
    
    # Keep only last 7 days
    cutoff_time = (datetime.now() - timedelta(days=7)).isoformat()
    conversions = [c for c in conversions if c['timestamp'] >= cutoff_time]
    
    with open(CONVERSIONS_FILE, 'w') as f:
        json.dump(conversions, f, indent=2)

def simple_decimate(mesh, target_ratio):
    """Simple face decimation by random sampling"""
    if not hasattr(mesh, 'faces') or len(mesh.faces) == 0:
        return mesh
    
    num_faces = len(mesh.faces)
    target_faces = max(int(num_faces * target_ratio), 10)
    
    if target_faces >= num_faces:
        return mesh
    
    np.random.seed(42)
    keep_indices = np.random.choice(num_faces, target_faces, replace=False)
    keep_indices = np.sort(keep_indices)
    
    new_faces = mesh.faces[keep_indices]
    unique_verts = np.unique(new_faces.flatten())
    vert_map = {old_idx: new_idx for new_idx, old_idx in enumerate(unique_verts)}
    remapped_faces = np.array([[vert_map[v] for v in face] for face in new_faces])
    new_vertices = mesh.vertices[unique_verts]
    
    return trimesh.Trimesh(vertices=new_vertices, faces=remapped_faces)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decimate_batch', methods=['POST'])
def decimate_batch():
    try:
        # Cleanup old files first
        cleanup_old_files()
        
        # Get uploaded files
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files[]')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        if len(files) > MAX_FILES:
            return jsonify({'error': f'Maximum {MAX_FILES} files allowed'}), 400
        
        # Get parameters
        reduction_level = request.form.get('reduction_level', 'medium')
        output_formats = request.form.getlist('output_formats[]')
        
        if not output_formats:
            return jsonify({'error': 'No output formats selected'}), 400
        
        for fmt in output_formats:
            if fmt not in SUPPORTED_FORMATS:
                return jsonify({'error': f'Invalid output format: {fmt}'}), 400
        
        # Process each file
        results = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for file in files:
            if file.filename == '':
                continue
            
            try:
                # Save uploaded file temporarily
                input_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(input_path)
                
                # Load mesh
                mesh = trimesh.load(input_path)
                
                if not hasattr(mesh, 'faces'):
                    results.append({
                        'filename': file.filename,
                        'status': 'error',
                        'message': 'File does not contain a valid mesh'
                    })
                    os.remove(input_path)
                    continue
                
                original_faces = len(mesh.faces)
                
                # Decimate mesh
                target_ratio = REDUCTION_LEVELS.get(reduction_level, 0.50)
                decimated_mesh = simple_decimate(mesh, target_ratio)
                decimated_faces = len(decimated_mesh.faces)
                
                # Get base filename
                base_name = Path(file.filename).stem
                
                # Export to selected formats
                output_files = []
                for fmt in output_formats:
                    output_filename = f"{base_name}_decimated_{reduction_level}_{timestamp}.{fmt}"
                    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
                    
                    decimated_mesh.export(output_path)
                    file_size = os.path.getsize(output_path)
                    
                    output_files.append({
                        'filename': output_filename,
                        'format': fmt,
                        'size': file_size
                    })
                
                # Clean up input file
                os.remove(input_path)
                
                # Calculate reduction percentage
                reduction_pct = round((1 - target_ratio) * 100, 1)
                
                results.append({
                    'filename': file.filename,
                    'status': 'success',
                    'original_faces': original_faces,
                    'decimated_faces': decimated_faces,
                    'reduction_percentage': reduction_pct,
                    'output_files': output_files
                })
                
                # Save conversion record
                save_conversion({
                    'timestamp': datetime.now().isoformat(),
                    'original_filename': file.filename,
                    'reduction_level': reduction_level,
                    'formats': output_formats,
                    'output_files': [f['filename'] for f in output_files],
                    'original_faces': original_faces,
                    'decimated_faces': decimated_faces
                })
                
            except Exception as e:
                results.append({
                    'filename': file.filename,
                    'status': 'error',
                    'message': str(e)
                })
                if os.path.exists(input_path):
                    os.remove(input_path)
        
        return jsonify({
            'status': 'success',
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/list_files')
def list_files():
    """List all files in output folder"""
    try:
        cleanup_old_files()
        
        files = []
        for filename in os.listdir(OUTPUT_FOLDER):
            filepath = os.path.join(OUTPUT_FOLDER, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    'filename': filename,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        # Sort by modified time, newest first
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download a specific file"""
    try:
        return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

@app.route('/download_all')
def download_all():
    """Download all files as ZIP"""
    try:
        cleanup_old_files()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_filename = f'all_conversions_{timestamp}.zip'
        zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir(OUTPUT_FOLDER):
                filepath = os.path.join(OUTPUT_FOLDER, filename)
                if os.path.isfile(filepath):
                    zipf.write(filepath, filename)
        
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/conversions_history')
def conversions_history():
    """Get conversion history (last 7 days)"""
    try:
        conversions = load_conversions()
        # Already filtered to 7 days in save_conversion
        return jsonify({'conversions': conversions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
