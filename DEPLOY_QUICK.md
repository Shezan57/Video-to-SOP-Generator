# 🎯 Quick Heroku Deploy - Copy & Paste Commands

## ⏱️ 5-Minute Deploy (After Student Pack Approval)

```powershell
# 1. Install Heroku CLI (one-time)
choco install heroku-cli

# 2. Login
heroku login

# 3. Navigate to project
cd d:\SHEZAN\AI\Video-to-SOP-Generator

# 4. Create app
heroku create video-sop-generator

# 5. Add buildpacks (ORDER MATTERS!)
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
heroku buildpacks:add --index 2 heroku/python

# 6. Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
# Copy the output

# 7. Set environment variables (replace with your actual keys)
heroku config:set SECRET_KEY=paste_generated_key_here
heroku config:set GROQ_API_KEY=your_groq_key_here
heroku config:set GEMINI_API_KEY=your_gemini_key_here

# 8. Deploy
git push heroku main

# 9. Initialize database
heroku run python -c "import sys; sys.path.insert(0, 'webapp'); from app import app, db; app.app_context().push(); db.create_all()"

# 10. Open your app
heroku open
```

## 🔑 Get Your API Keys

- **Groq**: https://console.groq.com/ (Free)
- **Gemini**: https://makersuite.google.com/app/apikey (Free)

## ✅ Done!

Your app is live at: `https://video-sop-generator.herokuapp.com`

---

## 🐛 If Something Goes Wrong

```powershell
# View logs
heroku logs --tail

# Restart
heroku restart

# Check buildpacks order
heroku buildpacks

# Reinitialize database
heroku run python -c "import sys; sys.path.insert(0, 'webapp'); from app import app, db; app.app_context().push(); db.drop_all(); db.create_all()"
```

---

For detailed guide, see: **HEROKU_DEPLOYMENT.md** 📖
