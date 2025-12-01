# Quick Start Guide - Video-to-SOP Generator v2.0 🚀

Get started in 5 minutes!

---

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Git installed (optional)
- [ ] FFmpeg installed ([Guide](FFMPEG_SETUP.md))
- [ ] Google Gemini API key ([Get here](https://makersuite.google.com/app/apikey))
- [ ] Groq API key ([Get here](https://console.groq.com/))

---

## Step-by-Step Setup

### 1. Install Python Dependencies

First, activate your virtual environment:

```powershell
# Windows PowerShell
.\myvenv\Scripts\Activate.ps1

# Or create new venv if needed
python -m venv myvenv
.\myvenv\Scripts\Activate.ps1
```

Then install the required packages:

```powershell
pip install -r requirements.txt
```

### 2. Install FFmpeg (for 15x faster processing!)

**Windows:**
```powershell
choco install ffmpeg
```

**Verify installation:**
```powershell
ffmpeg -version
```

See [FFMPEG_SETUP.md](FFMPEG_SETUP.md) for detailed instructions.

### 3. Set Up Your API Keys

1. Get your API keys:
   - **Gemini**: https://makersuite.google.com/app/apikey
   - **Groq**: https://console.groq.com/

2. Create a `.env` file in the project root:

```powershell
# Copy the example file
Copy-Item .env.example .env
```

3. Edit `.env` and add your API keys:

```
GOOGLE_API_KEY=your_google_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Prepare a Test Video

For your first test, use a short (30-60 second) video showing:
- A simple task or procedure
- Clear visibility of actions
- Good lighting

Name it `sample_video.mp4` or specify the path when running.

### 5. Generate Your First SOP

#### Basic usage:
```powershell
python main.py sample_video.mp4
```

#### With options:
```powershell
python main.py sample_video.mp4 `
  --output my_first_sop.pdf `
  --context "Widget assembly procedure" `
  --company "ACME Manufacturing"
```

### 6. Check the Output

Open the generated PDF file (`output_sop.pdf`) to see:
- Title page
- Table of contents
- Safety notes
- Step-by-step instructions with images

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"

**Solution:**
```powershell
# Check if .env exists
Test-Path .env

# If false, create it
Copy-Item .env.example .env

# Edit .env and add your key
notepad .env
```

### Issue: "Import cv2 could not be resolved"

**Solution:**
```powershell
pip install opencv-python
```

### Issue: "Import reportlab could not be resolved"

**Solution:**
```powershell
pip install reportlab
```

### Issue: Video processing is slow

**Options:**
1. Use `--direct-video` flag (faster, less control)
2. Use shorter videos for testing
3. Increase frame interval in `video_processor.py`

## Testing with Your Own Video

### Best Practices:

1. **Video Quality:**
   - 720p or higher resolution
   - 30 FPS minimum
   - Good lighting
   - Stable camera

2. **Video Content:**
   - Clear view of the task
   - Worker performs actions deliberately
   - No excessive movement
   - 1-5 minutes duration

3. **Context is Key:**
   - Provide context with `--context` flag
   - Example: "Hydraulic pump maintenance"
   - Helps AI understand the domain

### Example Commands:

```powershell
# Manufacturing assembly
python main.py assembly_video.mp4 `
  --context "PCB assembly process" `
  --company "TechCorp Manufacturing"

# Equipment maintenance
python main.py maintenance.mp4 `
  --context "Hydraulic system maintenance" `
  --company "Industrial Services Inc"

# Quality control
python main.py inspection.mp4 `
  --context "Visual quality inspection procedure" `
  --company "Quality Assurance Ltd"
```

## Next Steps

### Customize for Your Needs:

1. **Adjust Frame Extraction:**
   - Edit `video_processor.py`
   - Change `interval_seconds` (default: 1-2 seconds)

2. **Modify PDF Layout:**
   - Edit `pdf_generator.py`
   - Customize colors, fonts, layout

3. **Fine-tune AI Prompts:**
   - Edit `sop_analyzer.py`
   - Modify the system prompt for your industry

### Advanced Usage:

```powershell
# Use direct video upload (faster)
python main.py video.mp4 --direct-video

# Multiple videos in sequence
python main.py video1.mp4 -o sop1.pdf
python main.py video2.mp4 -o sop2.pdf
python main.py video3.mp4 -o sop3.pdf
```

## Performance Tips

- **Short videos (<2 min):** Use frame extraction mode
- **Long videos (>2 min):** Use `--direct-video` mode
- **Multiple videos:** Process them in parallel if you have multiple API keys
- **High quality needed:** Use frame extraction + manual review

## Cost Estimation

Gemini API Pricing (as of 2024):
- Free tier: 60 requests/minute
- Paid tier: Pay per token

Typical costs per video:
- 1-minute video: ~$0.05-0.15
- 5-minute video: ~$0.25-0.50

## Getting Help

1. Check the README.md
2. Review code comments
3. Test with `demo.py`
4. Check Gemini API status: https://status.google.com/

## Ready to Go!

You're all set! Start converting your training videos to professional SOPs.

```powershell
python main.py your_video.mp4
```

---

**Happy SOP Generation!** 🎥 → 📄
