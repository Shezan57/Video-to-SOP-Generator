# 🚀 Quick Start Guide - Web Application

## Get Started in 5 Minutes!

### Step 1: Activate Virtual Environment
```powershell
cd d:\SHEZAN\AI\Video-to-SOP-Generator
.\myvenv\Scripts\Activate.ps1
```

### Step 2: Verify Installation
```powershell
pip list | Select-String -Pattern "Flask"
```
You should see:
- Flask 3.1.2
- Flask-Login 0.6.3
- Flask-SQLAlchemy 3.1.1

### Step 3: Set Environment Variables
Create `.env` file in project root:
```
SECRET_KEY=your-secret-key-here-generate-with-python-secrets
GROQ_API_KEY=your-groq-api-key
GEMINI_API_KEY=your-gemini-api-key
```

**Generate SECRET_KEY**:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 4: Run the Application
```powershell
cd webapp
python app.py
```

### Step 5: Open in Browser
Navigate to: **http://localhost:5000**

---

## 🎯 First Time Usage

### 1. Register Account
- Click "Register" button
- Fill in:
  - Username: `testuser`
  - Email: `test@example.com`
  - Company Name: `Your Company Name` (will appear on PDFs)
  - Password: `password123` (min 6 characters)
  - Confirm Password: `password123`
- Click "Register"

### 2. Login
- Username: `testuser`
- Password: `password123`
- Check "Remember me" (optional)
- Click "Login"

### 3. Generate Your First SOP
- Click "Generate New SOP" from dashboard
- Upload a video file (MP4, AVI, MOV, WebM, MKV)
- Add optional context: `"This is a repair procedure for electronic equipment"`
- Click "Generate SOP"
- Wait ~2 minutes for processing

### 4. View and Download
- Automatically redirected to SOP details page
- Click "Download PDF" to get your SOP
- Return to dashboard to see all your SOPs

---

## 📁 Project Structure

```
Video-to-SOP-Generator/
├── webapp/                    # Web application
│   ├── app.py                # Main Flask app
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── generate.html
│   │   ├── view_sop.html
│   │   └── profile.html
│   ├── static/               # CSS and JavaScript
│   │   ├── css/style.css
│   │   └── js/main.js
│   ├── uploads/              # User uploaded videos
│   ├── generated_sops/       # Generated PDFs
│   └── README.md
├── main.py                   # CLI version (still works!)
├── video_processor.py        # FFmpeg frame extraction
├── sop_analyzer.py          # AI analysis
├── pdf_generator.py         # PDF creation
├── whisper_transcription.py # Audio transcription
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
├── Procfile                 # Heroku deployment
├── runtime.txt              # Python version
├── DEPLOYMENT.md            # Full deployment guide
├── WEB_APP_SUMMARY.md       # Implementation summary
└── README.md                # Main documentation
```

---

## 🔑 Features

### User Management
- ✅ Secure registration with password hashing
- ✅ Login with session management
- ✅ Company name for document branding
- ✅ User profile page
- ✅ Remember me functionality

### SOP Generation
- ✅ Drag-and-drop video upload
- ✅ Supports: MP4, AVI, MOV, WebM, MKV
- ✅ Max file size: 500MB
- ✅ Optional context input
- ✅ Real-time progress indicator
- ✅ Automatic processing with AI
- ✅ Professional PDF output

### Dashboard
- ✅ View all your SOPs
- ✅ Statistics (total SOPs, steps)
- ✅ Download PDFs
- ✅ Delete SOPs
- ✅ View SOP details
- ✅ Processing time tracking

---

## 🎨 Screenshots (What You'll See)

### Home Page
- Hero section with features
- "How It Works" guide
- Get Started / Login buttons

### Registration
- Username, email, password fields
- Company name (important!)
- Password confirmation
- Clean form validation

### Dashboard
- Welcome message with company name
- Statistics cards (Total SOPs, This Month, Total Steps)
- Table of all your SOPs
- Actions: View, Download, Delete

### Generate SOP
- File upload area (drag-and-drop)
- Context textarea
- Processing information
- Generate button

### View SOP
- SOP details (title, steps, processing time)
- Company information
- Download button
- Metadata table

---

## ⚡ Quick Commands

### Start Server
```powershell
.\myvenv\Scripts\Activate.ps1
cd webapp
python app.py
```

### Stop Server
Press `Ctrl+C` in terminal

### Reset Database (if needed)
```powershell
cd webapp
Remove-Item video_sop.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Check Logs
Flask runs in debug mode, logs appear in terminal

### Access Database
```powershell
cd webapp
python
>>> from app import app, db, User, SOP
>>> app.app_context().push()
>>> User.query.all()  # See all users
>>> SOP.query.all()   # See all SOPs
```

---

## 🐛 Troubleshooting

### "Module not found: flask_sqlalchemy"
**Solution**:
```powershell
.\myvenv\Scripts\Activate.ps1
pip install Flask Flask-SQLAlchemy Flask-Login Werkzeug gunicorn
```

### "Port 5000 already in use"
**Solution**: Change port in `webapp/app.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### "Upload failed"
**Solutions**:
- Check file size (max 500MB)
- Verify file format (MP4, AVI, MOV, WebM, MKV)
- Ensure `webapp/uploads/` directory exists
- Check disk space

### "API key not found"
**Solution**: Create `.env` file with:
```
GROQ_API_KEY=your-key-here
GEMINI_API_KEY=your-key-here
```

### "Database locked"
**Solution**: SQLite doesn't support concurrent writes. For production, use PostgreSQL:
```python
# In webapp/app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
```

---

## 🚀 Deploy to Heroku (Quick)

```bash
# 1. Login
heroku login

# 2. Create app
heroku create your-app-name

# 3. Add buildpacks
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
heroku buildpacks:add --index 2 heroku/python

# 4. Set environment variables
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
heroku config:set GROQ_API_KEY=your_key
heroku config:set GEMINI_API_KEY=your_key

# 5. Deploy
git push heroku main

# 6. Open app
heroku open
```

See **DEPLOYMENT.md** for detailed instructions!

---

## 📚 Learn More

- **Full Documentation**: See `webapp/README.md`
- **Deployment Guide**: See `DEPLOYMENT.md`
- **Implementation Details**: See `WEB_APP_SUMMARY.md`
- **Main Project**: See root `README.md`

---

## 💡 Tips

1. **Company Name**: Choose carefully - it appears on all your SOPs
2. **Video Quality**: Higher quality = better frame extraction
3. **Context**: Provide context for more accurate AI analysis
4. **Processing Time**: ~2 minutes for 4-minute video
5. **Storage**: Generated PDFs stay until you delete them

---

## 🎉 You're Ready!

Your web application is now running at: **http://localhost:5000**

1. ✅ Register your account
2. ✅ Upload a video
3. ✅ Generate your first SOP
4. ✅ Download the PDF
5. ✅ Deploy to cloud (optional)

**Enjoy your professional SOP generator!** 🚀

---

**Need Help?**
- Check terminal for error messages
- Review `DEPLOYMENT.md` for deployment issues
- Create GitHub issue for bugs
- Read `WEB_APP_SUMMARY.md` for technical details

**Repository**: https://github.com/Shezan57/Video-to-SOP-Generator
