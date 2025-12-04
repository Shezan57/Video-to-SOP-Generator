# Deployment Guide - Video to SOP Generator Web App

## 🚀 Deployment Options

This guide covers deploying the Video-to-SOP Generator web application to various platforms.

---

## Option 1: Heroku (Recommended)

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed
- Git repository

### Step-by-Step Deployment

1. **Install Heroku CLI**:
   ```bash
   # Windows (via Chocolatey)
   choco install heroku-cli
   
   # Or download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Heroku App**:
   ```bash
   cd d:\SHEZAN\AI\Video-to-SOP-Generator
   heroku create video-sop-generator-app
   # Replace 'video-sop-generator-app' with your preferred app name
   ```

4. **Add FFmpeg Buildpack** (Required for video processing):
   ```bash
   heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
   heroku buildpacks:add --index 2 heroku/python
   ```

5. **Set Environment Variables**:
   ```bash
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   heroku config:set GROQ_API_KEY=your_groq_api_key_here
   heroku config:set GEMINI_API_KEY=your_gemini_api_key_here
   ```

6. **Deploy to Heroku**:
   ```bash
   git push heroku main
   ```

7. **Initialize Database**:
   ```bash
   heroku run python -c "import sys; sys.path.insert(0, 'webapp'); from app import app, db; app.app_context().push(); db.create_all()"
   ```

8. **Open Your App**:
   ```bash
   heroku open
   ```

### Post-Deployment Configuration

**Scale Dynos** (for better performance):
```bash
heroku ps:scale web=1
```

**View Logs**:
```bash
heroku logs --tail
```

**Upgrade Database** (for production):
```bash
heroku addons:create heroku-postgresql:mini
```

Then update `webapp/app.py`:
```python
# Replace SQLite URI with PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///video_sop.db').replace('postgres://', 'postgresql://')
```

**Set Worker Timeout** (for long video processing):
```bash
heroku config:set WEB_CONCURRENCY=2
```

### Heroku Limitations on Free Tier
- **Dyno Sleep**: App sleeps after 30 minutes of inactivity
- **Monthly Hours**: 550 free dyno hours/month
- **File Storage**: Ephemeral (files deleted on restart)
- **Solution**: Upgrade to Hobby dyno ($7/month) or use cloud storage (AWS S3)

---

## Option 2: Render (Alternative to Heroku)

### Prerequisites
- Render account (free tier available)
- GitHub repository

### Deployment Steps

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create New Web Service on Render**:
   - Go to https://render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: video-sop-generator
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn --chdir webapp app:app --timeout 300`

3. **Add Environment Variables**:
   - `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
   - `GROQ_API_KEY`: Your Groq API key
   - `GEMINI_API_KEY`: Your Gemini API key
   - `PYTHON_VERSION`: 3.11.0

4. **Deploy**: Click "Create Web Service"

5. **Access Your App**: Render will provide a URL like `https://video-sop-generator.onrender.com`

### Render Advantages
- ✅ No dyno sleep on free tier (50 GB bandwidth/month)
- ✅ Automatic deploys from GitHub
- ✅ Built-in SSL certificates
- ✅ Persistent disk storage available

---

## Option 3: AWS EC2 (Production-Grade)

### Prerequisites
- AWS account
- EC2 instance (Ubuntu recommended)
- SSH access

### Deployment Steps

1. **Launch EC2 Instance**:
   - Instance Type: t2.medium or higher
   - AMI: Ubuntu 22.04 LTS
   - Security Group: Allow HTTP (80), HTTPS (443), SSH (22)

2. **Connect to Instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-public-ip
   ```

3. **Install Dependencies**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3.11 python3.11-venv python3-pip ffmpeg nginx -y
   ```

4. **Clone Repository**:
   ```bash
   cd /home/ubuntu
   git clone https://github.com/Shezan57/Video-to-SOP-Generator.git
   cd Video-to-SOP-Generator
   ```

5. **Setup Python Environment**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configure Environment Variables**:
   ```bash
   nano .env
   # Add your keys
   ```

7. **Setup Gunicorn as Systemd Service**:
   ```bash
   sudo nano /etc/systemd/system/video-sop.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Video to SOP Generator
   After=network.target

   [Service]
   User=ubuntu
   Group=ubuntu
   WorkingDirectory=/home/ubuntu/Video-to-SOP-Generator/webapp
   Environment="PATH=/home/ubuntu/Video-to-SOP-Generator/venv/bin"
   ExecStart=/home/ubuntu/Video-to-SOP-Generator/venv/bin/gunicorn --chdir /home/ubuntu/Video-to-SOP-Generator/webapp app:app --bind 127.0.0.1:5000 --workers 4 --timeout 300

   [Install]
   WantedBy=multi-user.target
   ```

8. **Start Service**:
   ```bash
   sudo systemctl start video-sop
   sudo systemctl enable video-sop
   sudo systemctl status video-sop
   ```

9. **Configure Nginx**:
   ```bash
   sudo nano /etc/nginx/sites-available/video-sop
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           client_max_body_size 500M;
       }
   }
   ```

   Enable site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/video-sop /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

10. **Setup SSL with Let's Encrypt**:
    ```bash
    sudo apt install certbot python3-certbot-nginx -y
    sudo certbot --nginx -d your-domain.com
    ```

### AWS S3 for File Storage (Optional)

Update `webapp/app.py` to use S3 for uploads and generated PDFs:

```python
import boto3

s3_client = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
    region_name=os.getenv('AWS_REGION')
)

# Upload to S3 instead of local storage
def upload_to_s3(file_path, bucket, key):
    s3_client.upload_file(file_path, bucket, key)
    return f"https://{bucket}.s3.amazonaws.com/{key}"
```

---

## Option 4: Docker (Container Deployment)

### Create Dockerfile

Create `Dockerfile` in project root:
```dockerfile
FROM python:3.11-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--chdir", "webapp", "app:app", "--bind", "0.0.0.0:5000", "--timeout", "300", "--workers", "2"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./webapp/uploads:/app/webapp/uploads
      - ./webapp/generated_sops:/app/webapp/generated_sops
      - ./webapp/video_sop.db:/app/webapp/video_sop.db
    restart: unless-stopped
```

### Deploy with Docker

```bash
# Build image
docker-compose build

# Run container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down
```

---

## Environment Variables

All deployment options require these environment variables:

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Flask secret key for sessions | Yes | `a7f9c8b2e4d1f6g3h8j5k9m2n7p4q1r6` |
| `GROQ_API_KEY` | Groq API key for Whisper | Yes | `gsk_xxxxx` |
| `GEMINI_API_KEY` | Google Gemini API key | Yes | `AIzaSyxxxxx` |
| `DATABASE_URL` | PostgreSQL connection (optional) | No | `postgresql://user:pass@host/db` |
| `AWS_ACCESS_KEY` | AWS access key (for S3) | No | `AKIAXXXXX` |
| `AWS_SECRET_KEY` | AWS secret key (for S3) | No | `xxxxx` |
| `AWS_REGION` | AWS region | No | `us-east-1` |

---

## Post-Deployment Checklist

- [ ] Test user registration
- [ ] Test user login
- [ ] Test video upload (small file first)
- [ ] Test SOP generation
- [ ] Test PDF download
- [ ] Monitor server logs for errors
- [ ] Set up monitoring (New Relic, DataDog)
- [ ] Configure backups for database
- [ ] Set up error tracking (Sentry)
- [ ] Enable HTTPS/SSL
- [ ] Configure CDN (Cloudflare)
- [ ] Set up scheduled database backups

---

## Troubleshooting

### Issue: Upload timeout
**Solution**: Increase timeout in Procfile/Gunicorn config:
```
web: gunicorn --chdir webapp app:app --timeout 600 --workers 2
```

### Issue: Out of memory
**Solution**: 
- Reduce number of workers
- Upgrade dyno/instance size
- Process videos in batches

### Issue: Database connection error
**Solution**: Check `DATABASE_URL` format:
```python
# Heroku postgres format fix
db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
```

### Issue: FFmpeg not found
**Solution**: Ensure FFmpeg buildpack is added first:
```bash
heroku buildpacks
# Should show ffmpeg before python
```

---

## Monitoring & Maintenance

### Heroku Logs
```bash
heroku logs --tail --app your-app-name
```

### Database Backup
```bash
heroku pg:backups:capture --app your-app-name
heroku pg:backups:download --app your-app-name
```

### Performance Monitoring
Add New Relic:
```bash
heroku addons:create newrelic:wayne
```

---

## Cost Estimates

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Heroku** | 550 hrs/month | $7-25/month | Quick setup |
| **Render** | 750 hrs/month | $7-25/month | Auto-deploy |
| **AWS EC2** | 750 hrs (t2.micro) | $10-50/month | Full control |
| **Docker** | N/A | Server cost | Portability |

---

## Security Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use strong SECRET_KEY** - Generate with `secrets.token_hex(32)`
3. **Enable HTTPS** - Use Let's Encrypt or platform SSL
4. **Rate limiting** - Consider Flask-Limiter
5. **File validation** - Already implemented in app.py
6. **SQL injection protection** - SQLAlchemy handles this
7. **XSS protection** - Jinja2 auto-escapes templates

---

## Support

For deployment issues:
1. Check platform-specific documentation
2. Review application logs
3. Create GitHub issue with logs and steps to reproduce

---

**Congratulations!** Your Video-to-SOP Generator web app is now deployed! 🎉
