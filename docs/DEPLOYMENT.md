# Deployment Guide

Complete deployment instructions for 3D Decimator.

## Quick Deploy with Docker

```bash
# Clone the repository
git clone https://github.com/yourusername/3d-decimator.git
cd 3d-decimator

# Deploy with Docker Compose
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f

# Access the application
open http://localhost:8002
```

## Manual Docker Deployment

```bash
# Build the image
docker build -t 3d-decimator .

# Run the container
docker run -d \
  --name 3d-decimator \
  --restart unless-stopped \
  -p 8002:8000 \
  -v $(pwd)/outputs:/app/outputs \
  3d-decimator

# Check logs
docker logs -f 3d-decimator

# Stop/restart
docker stop 3d-decimator
docker start 3d-decimator
```

## Production Deployment (VPS)

### Prerequisites
- Ubuntu 22.04+ server
- Docker installed
- Port 8002 available

### Deployment Steps

1. **Connect to VPS**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install Docker** (if not installed)
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

3. **Clone and Deploy**
   ```bash
   git clone https://github.com/yourusername/3d-decimator.git
   cd 3d-decimator
   
   docker build -t 3d-decimator .
   
   docker run -d \
     --name 3d-decimator \
     --restart unless-stopped \
     -p 8002:8000 \
     -v /opt/3d-decimator/outputs:/app/outputs \
     3d-decimator
   ```

4. **Verify Deployment**
   ```bash
   docker ps | grep 3d-decimator
   docker logs 3d-decimator
   curl http://localhost:8002/health
   ```

### Updating

```bash
cd 3d-decimator
git pull origin main

docker stop 3d-decimator
docker rm 3d-decimator

docker build -t 3d-decimator .

docker run -d \
  --name 3d-decimator \
  --restart unless-stopped \
  -p 8002:8000 \
  -v /opt/3d-decimator/outputs:/app/outputs \
  3d-decimator
```

## Configuration

### Environment Variables

Create a `.env` file:

```env
UPLOAD_FOLDER=/app/uploads
OUTPUT_FOLDER=/app/outputs
MAX_FILE_SIZE=104857600
MAX_FILES=20
RETENTION_DAYS=5
```

Then run with:
```bash
docker run -d \
  --name 3d-decimator \
  --env-file .env \
  -p 8002:8000 \
  -v $(pwd)/outputs:/app/outputs \
  3d-decimator
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs 3d-decimator

# Common issues:
# - Port already in use: Change -p 8002:8000 to -p XXXX:8000
# - Permission issues: Check volume mount paths
```

### Health Check Failing

```bash
# Test health endpoint
docker exec 3d-decimator curl http://localhost:8000/health

# Expected: {"status":"healthy"}
```

### Files Not Persisting

```bash
# Verify volume mount
docker inspect 3d-decimator | grep Mounts -A 20

# Check host directory
ls -lh ./outputs/
```

## Performance Tuning

### For Large Files

Increase Gunicorn timeout in Dockerfile:
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "600", "app:app"]
```

### For High Traffic

Increase workers:
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "300", "app:app"]
```

## Monitoring

### View Logs

```bash
# Real-time logs
docker logs -f 3d-decimator

# Last 100 lines
docker logs --tail 100 3d-decimator
```

### Check Resource Usage

```bash
docker stats 3d-decimator
```

### Check Disk Usage

```bash
# Check output directory size
du -sh outputs/

# List files older than 5 days (should auto-delete)
find outputs/ -type f -mtime +5
```

## Security

### Enable HTTPS

Use a reverse proxy like Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then add SSL with Let's Encrypt:
```bash
sudo certbot --nginx -d your-domain.com
```

## Backup

### Backup Outputs

```bash
# Create backup
tar -czf outputs-backup-$(date +%Y%m%d).tar.gz outputs/

# Restore
tar -xzf outputs-backup-YYYYMMDD.tar.gz
```

## Support

For deployment issues:
- Check the main [README](../README.md)
- Open an issue on GitHub
- Review Docker logs first

---

**Deployed successfully?** Access your instance at http://your-server-ip:8002 🚀
