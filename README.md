# 3D Decimator

A powerful web-based tool for reducing 3D mesh complexity while preserving visual quality. Features batch processing, multi-format support, and an intuitive web interface.

![Version](https://img.shields.io/badge/version-3.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)

## ✨ Features

- **Batch Processing**: Process up to 20 files simultaneously
- **Multi-Format Support**: STL, OBJ, and 3MF input/output with format conversion
- **Three Reduction Levels**: Light (25%), Medium (50%), Heavy (75%)
- **File Browser**: Browse and download all converted files
- **Conversion History**: Track all conversions from the last 7 days
- **Auto-Cleanup**: Automatic file deletion after 5 days
- **Responsive UI**: Clean, modern 3-tab interface
- **Docker Ready**: Easy deployment with Docker

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/3d-decimator.git
cd 3d-decimator

# Build the Docker image
docker build -t 3d-decimator .

# Run the container
docker run -d \
  --name 3d-decimator \
  --restart unless-stopped \
  -p 8002:8000 \
  -v $(pwd)/outputs:/app/outputs \
  3d-decimator

# Access the application
open http://localhost:8002
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/3d-decimator.git
cd 3d-decimator

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access at http://localhost:8000
```

## 📖 Usage

### Basic Workflow

1. **Upload**: Click or drag 3D files (STL, OBJ, 3MF) onto the upload area
2. **Configure**: Select reduction level and output formats
3. **Process**: Click "Process & Download" 
4. **Download**: Get your reduced files individually or as a ZIP

### Batch Processing

1. Select multiple files (up to 20)
2. Drag them all onto the upload area
3. Choose settings (applies to all files)
4. Process and download results

### File Browser

- View all converted files with sizes and dates
- Download individual files
- Download all files as a ZIP
- Files auto-delete after 5 days

## 🛠️ Configuration

### Environment Variables

```bash
UPLOAD_FOLDER=/app/uploads          # Temporary upload directory
OUTPUT_FOLDER=/app/outputs          # Persistent output directory
MAX_FILE_SIZE=104857600             # 100 MB in bytes
MAX_FILES=20                        # Maximum batch size
RETENTION_DAYS=5                    # File retention period
```

### Reduction Levels

| Level  | Reduction | Best For                              |
|--------|-----------|---------------------------------------|
| Light  | 25%       | Preserving fine details               |
| Medium | 50%       | Balanced reduction (default)          |
| Heavy  | 75%       | Maximum size reduction for previews   |

## 🐳 Docker Deployment

### Production Deployment

```bash
docker run -d \
  --name 3d-decimator \
  --restart unless-stopped \
  -p 8002:8000 \
  -v /path/to/outputs:/app/outputs \
  3d-decimator
```

### Docker Compose

```yaml
version: '3.8'
services:
  decimator:
    build: .
    container_name: 3d-decimator
    restart: unless-stopped
    ports:
      - "8002:8000"
    volumes:
      - ./outputs:/app/outputs
```

## 📁 Project Structure

```
3d-decimator/
├── app.py              # Flask application with batch processing
├── templates/
│   └── index.html      # 3-tab UI (Upload, Browser, History)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container definition
├── docs/
│   └── DEPLOYMENT.md   # Detailed deployment guide
└── README.md          # This file
```

## 🔧 Technical Specifications

- **Framework**: Flask 3.0
- **Mesh Processing**: Trimesh 4.0.10
- **Server**: Gunicorn with 300s timeout
- **Storage**: Persistent volume for outputs
- **History**: JSON-based conversion tracking

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Developed by japsmalata

## 📞 Support

For issues, questions, or feedback:
- Open an issue on GitHub
- Contact: John Kenneth M. Marquez

## 🔄 Version History

- **v3.0** (April 2026) - Batch processing, file browser, history tracking, auto-cleanup
- **v2.0** (April 2026) - Multi-format support (STL, OBJ, 3MF), format conversion
- **v1.0** (February 2026) - Initial release - STL format only

---

**Made with ❤️ by japsmalata**
