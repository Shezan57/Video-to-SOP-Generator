# 🚀 Heroku Deployment Guide - Video to SOP Generator

## 📋 Prerequisites

- ✅ Heroku Student Pack approved (wait 24 hours)
- ✅ Git installed
- ✅ Code pushed to GitHub
- ✅ API keys ready (Groq + Gemini)

---

## Step 1: Install Heroku CLI

**Windows:**
```powershell
# Option A: Download installer
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Option B: Using Chocolatey
choco install heroku-cli

# Option C: Using Scoop
scoop install heroku-cli
```

**Verify installation:**
```powershell
heroku --version
# Should show: heroku/8.x.x win32-x64 node-v18.x.x
```

---

## Step 2: Login to Heroku

```powershell
heroku login
```

This will open your browser. Login with your Heroku account (the one with Student Pack).

---

## Step 3: Create Heroku App

```powershell
cd d:\SHEZAN\AI\Video-to-SOP-Generator

# Create app (choose unique name)
heroku create video-sop-generator

# Or let Heroku generate random name
heroku create

# Note: Your app URL will be: https://your-app-name.herokuapp.com
```

---

## Step 4: Add FFmpeg Buildpack (CRITICAL!)

FFmpeg is required for video processing. Add it BEFORE Python buildpack:

```powershell
# Add FFmpeg buildpack first (index 1)
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git

# Add Python buildpack second (index 2)
heroku buildpacks:add --index 2 heroku/python

# Verify buildpacks order
heroku buildpacks
# Should show:
# 1. https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
# 2. heroku/python
```

---

## Step 5: Generate SECRET_KEY

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output (e.g., `a7f9c8b2e4d1f6g3h8j5k9m2n7p4q1r6s8t0u5v7w9x2y4z1`)

---

## Step 6: Set Environment Variables

Replace the placeholder values with your actual keys:

```powershell
# Set SECRET_KEY (use the one generated above)
heroku config:set SECRET_KEY=a7f9c8b2e4d1f6g3h8j5k9m2n7p4q1r6s8t0u5v7w9x2y4z1

# Set GROQ API Key (get from https://console.groq.com/)
heroku config:set GROQ_API_KEY=gsk_your_groq_api_key_here

# Set GEMINI API Key (get from https://makersuite.google.com/app/apikey)
heroku config:set GEMINI_API_KEY=AIzaSy_your_gemini_api_key_here

# Verify environment variables
heroku config
```

---

## Step 7: Deploy to Heroku

```powershell
# Make sure you're on main branch
git branch
# Should show: * main

# Push to Heroku
git push heroku main
```

**Deployment will:**
1. Install FFmpeg buildpack (~2 minutes)
2. Install Python dependencies (~3 minutes)
3. Start your app with Gunicorn

**Expected output:**
```
-----> Building on the Heroku-22 stack
-----> Using buildpack: https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
-----> FFmpeg app detected
-----> Installing ffmpeg
-----> Python app detected
-----> Installing python-3.11.0
-----> Installing pip 23.x, setuptools 68.x and wheel 0.41.x
-----> Installing SQLite3
-----> Installing requirements with pip
       Collecting Flask==3.0.0
       ...
-----> Discovering process types
       Procfile declares types -> web
-----> Compressing...
-----> Launching...
       Released v3
       https://video-sop-generator.herokuapp.com/ deployed to Heroku
```

---

## Step 8: Initialize Database

After successful deployment, create the database tables:

```powershell
heroku run python -c "import sys; sys.path.insert(0, 'webapp'); from app import app, db; app.app_context().push(); db.create_all()"
```

**Expected output:**
```
Running python -c "..." on ⬢ video-sop-generator... up, run.1234 (Free)
# No errors = success!
```

---

## Step 9: Open Your App

```powershell
heroku open
```

This opens your app in the browser: `https://your-app-name.herokuapp.com`

---

## Step 10: Test Your Deployment

1. **Home Page**: Should load with features and "Get Started" button
2. **Register**: Create a new account
3. **Login**: Login with your credentials
4. **Dashboard**: Should show empty state "No SOPs Yet"
5. **Generate SOP**: Upload a small test video (under 50MB for first test)
6. **Wait**: Processing takes ~2 minutes for 4-minute video
7. **Download**: Check if PDF generates correctly with your company name

---

## 🔍 Monitoring & Troubleshooting

### View Logs (Real-time)
```powershell
heroku logs --tail
```

**Common log messages:**
- `Booting worker with pid` = App started successfully
- `GET / 200` = Home page loaded
- `POST /register 302` = User registered
- `POST /login 302` = User logged in
- `POST /generate 200` = SOP generation started

### View Logs (Last 100 lines)
```powershell
heroku logs -n 100
```

### Check App Status
```powershell
heroku ps
```

**Expected output:**
```
=== web (Free): gunicorn --chdir webapp app:app (1)
web.1: up 2024/12/03 10:30:45 +0000 (~ 5m ago)
```

### Restart App
```powershell
heroku restart
```

### Check Environment Variables
```powershell
heroku config
```

---

## 🐛 Common Issues & Solutions

### Issue 1: App Crashes Immediately

**Check logs:**
```powershell
heroku logs --tail
```

**Common causes:**
- Missing environment variables → Set SECRET_KEY, GROQ_API_KEY, GEMINI_API_KEY
- Database not initialized → Run database creation command
- Port binding issue → Procfile should use `$PORT` (already configured)

### Issue 2: FFmpeg Not Found

**Check buildpacks order:**
```powershell
heroku buildpacks
```

**Fix:** FFmpeg must be FIRST (index 1):
```powershell
heroku buildpacks:clear
heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
heroku buildpacks:add heroku/python
git commit --allow-empty -m "Rebuild with correct buildpacks"
git push heroku main
```

### Issue 3: Upload Timeout

**Increase timeout:**
```powershell
heroku config:set WEB_TIMEOUT=600
```

**Or edit Procfile locally and redeploy:**
```
web: gunicorn --chdir webapp app:app --timeout 600 --workers 2
```

### Issue 4: Database Error

**Reinitialize database:**
```powershell
heroku run python -c "import sys; sys.path.insert(0, 'webapp'); from app import app, db; app.app_context().push(); db.drop_all(); db.create_all()"
```

### Issue 5: Out of Memory

**Check dyno metrics:**
```powershell
heroku ps:type
```

**Upgrade to Hobby dyno** (included with Student Pack):
```powershell
heroku ps:type hobby
```

---

## 📊 Student Pack Benefits

With Heroku Student Pack, you get:

- ✅ **1 Free Hobby Dyno** ($7/month value)
  - No sleep (unlike free tier)
  - SSL certificate included
  - Custom domain support
  
- ✅ **Credits**: Additional Heroku credits
  
- ✅ **No Credit Card Required** for Hobby tier

**To activate Hobby dyno:**
```powershell
heroku ps:type hobby
```

---

## 🔐 Security Checklist

- ✅ SECRET_KEY is strong random string (32+ characters)
- ✅ API keys are set as environment variables (not in code)
- ✅ .env file is in .gitignore (already done)
- ✅ Database is SQLite (upgrade to PostgreSQL for production)
- ✅ HTTPS is enabled by default on Heroku

---

## 🚀 Performance Optimization

### Enable Preboot (Hobby dyno only)
```powershell
heroku features:enable preboot
```

### Add PostgreSQL (Better than SQLite for multiple users)
```powershell
# Add free PostgreSQL database
heroku addons:create heroku-postgresql:mini

# Get database URL
heroku config:get DATABASE_URL
```

**Update `webapp/app.py`:**
```python
import os

# Replace SQLite config with:
db_url = os.getenv('DATABASE_URL', 'sqlite:///video_sop.db')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
```

### Scale Workers
```powershell
# Check current
heroku ps

# Scale to 2 workers (better performance)
heroku ps:scale web=1
```

---

## 📈 Monitoring

### Add Papertrail (Free log management)
```powershell
heroku addons:create papertrail:choklad
heroku addons:open papertrail
```

### View Metrics
```powershell
heroku ps:type
heroku ps:status
```

---

## 🔄 Updating Your App

When you make code changes:

```powershell
# 1. Make your changes
# 2. Commit
git add .
git commit -m "Description of changes"

# 3. Push to GitHub
git push origin main

# 4. Push to Heroku
git push heroku main

# App will automatically rebuild and restart
```

---

## 🌐 Custom Domain (Optional)

If you have a domain:

```powershell
# Add domain
heroku domains:add www.yourdomain.com

# Get DNS target
heroku domains

# Add CNAME record at your domain provider:
# Type: CNAME
# Name: www
# Value: xxx-xxx-xxxxx.herokudns.com
```

---

## 💾 Backup Database

**Manual backup:**
```powershell
heroku pg:backups:capture
heroku pg:backups:download
```

**Schedule automatic backups:**
```powershell
heroku pg:backups:schedule DATABASE_URL --at '02:00 America/New_York'
```

---

## 📞 Support

**Heroku Status:**
https://status.heroku.com/

**Documentation:**
https://devcenter.heroku.com/

**Student Pack:**
https://education.github.com/pack

**Project Issues:**
https://github.com/Shezan57/Video-to-SOP-Generator/issues

---

## ✅ Deployment Checklist

Before going live:

- [ ] Student Pack approved
- [ ] Heroku CLI installed
- [ ] App created on Heroku
- [ ] FFmpeg buildpack added (index 1)
- [ ] Python buildpack added (index 2)
- [ ] SECRET_KEY generated and set
- [ ] GROQ_API_KEY set
- [ ] GEMINI_API_KEY set
- [ ] Code pushed to Heroku
- [ ] Database initialized
- [ ] App tested (register, login, upload, generate, download)
- [ ] Logs checked for errors
- [ ] Hobby dyno activated (if available)

---

## 🎉 You're Done!

Your Video-to-SOP Generator is now live on Heroku!

**Your app URL:** `https://your-app-name.herokuapp.com`

**Share it with:**
- Teammates
- Clients
- Portfolio
- LinkedIn

---

## 📝 Quick Reference

```powershell
# View logs
heroku logs --tail

# Restart app
heroku restart

# Check status
heroku ps

# View config
heroku config

# Open app
heroku open

# Run command
heroku run python --version

# Scale
heroku ps:scale web=1

# Upgrade dyno
heroku ps:type hobby
```

---

**Ready to deploy?** Just run through Steps 1-10 when your Student Pack is approved! 🚀
