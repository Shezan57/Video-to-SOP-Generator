#  SIMPLE FRONTEND SETUP GUIDE

##  What Was Created?
A complete Flask web application with:
- Login/Registration (with Company Name field)
- User Dashboard
- Video Upload
- SOP Generation with Progress
- PDF Download with YOUR company branding

##  3 SIMPLE STEPS TO RUN

### Step 1: Install Dependencies
`powershell
cd frontend
pip install -r requirements.txt
`

### Step 2: Create .env File
`powershell
cd frontend
Copy-Item .env.example .env
`
Then open .env and add your API keys:
`
SECRET_KEY=any-random-string-here
GOOGLE_API_KEY=your-google-api-key
GROQ_API_KEY=your-groq-api-key
`

### Step 3: Run the App
`powershell
cd frontend
python app.py
`

Open browser: http://localhost:5000

##  HOW TO USE

1. **Register** - Enter username, email, **COMPANY NAME**, password
2. **Login** - Use your username and password
3. **Generate SOP** - Upload video, enter title, click Generate
4. **Download** - Get your PDF with company branding!

##  Files Created

`
frontend/
 app.py              # Main Flask app
 config.py           # Settings
 models.py           # Database (User, SOP)
 requirements.txt    # Dependencies
 .env.example        # Environment template
 templates/          # HTML pages (8 files)
 static/            # CSS & JS
 uploads/           # Videos go here
 outputs/           # PDFs go here
`

##  Deployment (Later)

1. Push to GitHub
2. Deploy to Render.com or Railway.app (free)
3. Add environment variables there

##  Troubleshooting

**Error: Module not found?**
`powershell
pip install -r requirements.txt
cd frontend
pip install -r requirements.txt
`

**Error: API keys not found?**
Create rontend/.env with your keys.

**Port 5000 busy?**
Edit app.py line 167: change port to 5001

That's it! Simple! 
