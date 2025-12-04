# 🎥 Video-to-SOP Generator - Complete System Overview

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VIDEO-TO-SOP GENERATOR                   │
│                      (Main Application)                      │
└─────────────────────────────────────────────────────────────┘
                              |
                              |
        ┌─────────────────────┴─────────────────────┐
        |                     |                      |
        v                     v                      v
┌───────────────┐    ┌────────────────┐    ┌────────────────┐
│   VIDEO       │    │   AI           │    │   PDF          │
│   PROCESSOR   │    │   ANALYZER     │    │   GENERATOR    │
│               │    │                │    │                │
│  OpenCV +     │    │  Gemini 1.5    │    │  ReportLab     │
│  MoviePy      │    │  Pro API       │    │  + Pillow      │
└───────────────┘    └────────────────┘    └────────────────┘
```

---

## 🔄 Processing Pipeline

### Input → Process → Output

```
1. VIDEO INPUT
   ├─ User uploads: training_video.mp4
   └─ System validates: format, size, integrity

2. FRAME EXTRACTION (video_processor.py)
   ├─ Read video properties (FPS, duration, resolution)
   ├─ Extract frames every 1-2 seconds
   ├─ Resize to optimal size (512px width)
   ├─ Convert to base64 for API
   └─ Save timestamps for each frame

3. AI ANALYSIS (sop_analyzer.py)
   ├─ Send frames/video to Gemini API
   ├─ Use specialized SOP prompt
   ├─ AI identifies distinct actions
   ├─ AI writes step-by-step instructions
   ├─ AI selects best timestamp per step
   └─ Return structured JSON

4. PDF GENERATION (pdf_generator.py)
   ├─ Create title page
   ├─ Add table of contents
   ├─ Insert safety notes
   ├─ For each step:
   │   ├─ Extract frame at timestamp
   │   ├─ Add step number & instruction
   │   ├─ Insert screenshot
   │   └─ Add notes/reasoning
   └─ Save professional PDF

5. OUTPUT
   └─ Professional SOP manual: output_sop.pdf
```

---

## 📁 File Structure & Responsibilities

### Core Modules

#### 1. `main.py` - Application Controller
```python
VideoToSOPGenerator
├─ Orchestrates entire pipeline
├─ Handles command-line arguments
├─ Manages error handling
└─ Provides progress feedback
```

#### 2. `video_processor.py` - Video Handler
```python
VideoFrameExtractor
├─ extract_frames()           # Get frames from video
├─ get_video_info()          # Video metadata
├─ extract_frame_at_timestamp() # Single frame extraction
└─ _resize_frame()           # Image optimization
```

#### 3. `sop_analyzer.py` - AI Brain
```python
SOPAnalyzer
├─ analyze_video_frames()     # Frame-by-frame analysis
├─ analyze_video_file_directly() # Direct video upload
├─ _create_prompt()           # Prompt engineering
└─ _parse_response()          # JSON validation
```

#### 4. `pdf_generator.py` - Document Creator
```python
SOPPDFGenerator
├─ generate_sop_pdf()         # Main PDF creation
├─ _create_title_page()       # Title page layout
├─ _create_table_of_contents() # TOC generation
├─ _create_safety_section()   # Safety notes
├─ _create_steps_section()    # Procedure steps
└─ _setup_custom_styles()     # PDF styling
```

### Supporting Files

- `demo.py` - Testing suite
- `requirements.txt` - Dependencies
- `.env` - API keys (you create this)
- `README.md` - Documentation
- `QUICKSTART.md` - Setup guide
- `CHECKLIST.md` - Setup checklist

---

## 🎯 Data Flow

### JSON Structure (AI Output)

```json
{
  "title": "Engine Assembly Procedure",
  "description": "Complete assembly process for Model X engine",
  "safety_notes": [
    "Wear safety glasses at all times",
    "Ensure proper ventilation"
  ],
  "steps": [
    {
      "step_number": 1,
      "instruction": "Pick up the 5mm Allen wrench from tool tray",
      "timestamp_seconds": 12.5,
      "reasoning": "This tool is required for bolt assembly"
    },
    {
      "step_number": 2,
      "instruction": "Insert bolt into mounting hole",
      "timestamp_seconds": 25.0,
      "reasoning": "Ensure proper alignment before tightening"
    }
  ]
}
```

---

## 🛠️ Technology Stack

### Language & Runtime
- **Python 3.8+** - Core language
- **Virtual Environment (myvenv)** - Isolated dependencies

### Video Processing
- **OpenCV (cv2)** - Frame extraction, image manipulation
- **MoviePy** - Advanced video operations
- **NumPy** - Numerical operations for images

### AI & Machine Learning
- **Google Gemini 1.5 Pro** - Multimodal AI (vision + language)
- **google-generativeai** - Python SDK for Gemini

### PDF Generation
- **ReportLab** - PDF creation and layout
- **Pillow (PIL)** - Image processing and insertion

### Utilities
- **python-dotenv** - Environment variable management
- **tqdm** - Progress bars
- **requests** - HTTP requests (if needed)

---

## 💾 Storage & Files

### Input Files
```
user_video.mp4              # Original training video
.env                        # API keys (created by you)
```

### Temporary Files (Auto-cleaned)
```
extracted_frames/           # Frame images (optional)
  ├─ frame_000000.jpg
  ├─ frame_000060.jpg
  └─ frame_000120.jpg
temp_step_1.jpg            # Temporary step images
temp_step_2.jpg
```

### Output Files
```
output_sop.pdf             # Final SOP manual
```

---

## ⚙️ Configuration Options

### Environment Variables (`.env`)
```bash
GEMINI_API_KEY=AIzaSy...     # Required: Gemini API key
OPENAI_API_KEY=sk-...        # Optional: If using GPT-4o
```

### Video Processor Settings
```python
VideoFrameExtractor(
    interval_seconds=2,      # 1-3 seconds recommended
    resize_width=512        # 512-1024 pixels
)
```

### AI Analyzer Settings
```python
generation_config={
    "temperature": 0.4,      # 0.0 = deterministic, 1.0 = creative
    "max_output_tokens": 8192 # Response length limit
}
```

### PDF Generator Settings
```python
SOPPDFGenerator(
    page_size=letter         # letter or A4
)
```

---

## 🔐 Security & Privacy

### API Keys
- ✅ Stored in `.env` file (not committed to git)
- ✅ Loaded at runtime only
- ✅ Never logged or displayed

### Data Handling
- ✅ Videos processed locally
- ✅ Only frames sent to API (not full video by default)
- ✅ No permanent storage on Google servers
- ✅ Temporary files auto-cleaned

### Best Practices
- Keep `.env` file secure
- Don't share API keys
- Review generated SOPs before deployment
- Monitor API usage for costs

---

## 📊 Performance Metrics

### Processing Time
```
Video Length    |  Frame Mode  |  Direct Mode
----------------|--------------|-------------
30 seconds      |  ~30 sec     |  ~20 sec
1 minute        |  ~45 sec     |  ~30 sec
2 minutes       |  ~90 sec     |  ~45 sec
5 minutes       |  ~3 min      |  ~90 sec
```

### API Costs (Approximate)
```
Video Length    |  Tokens Used  |  Cost (USD)
----------------|---------------|-------------
30 seconds      |  ~5,000       |  $0.05
1 minute        |  ~10,000      |  $0.10
2 minutes       |  ~20,000      |  $0.20
5 minutes       |  ~50,000      |  $0.50
```

### Output Quality
- **Frame extraction mode**: Higher quality, more control
- **Direct video mode**: Faster, AI decides frames

---

## 🎨 PDF Output Structure

```
┌─────────────────────────────────────┐
│         TITLE PAGE                  │
│  • Company Name                     │
│  • SOP Title                        │
│  • Description                      │
│  • Document Info                    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│    TABLE OF CONTENTS                │
│  1. Safety Information         p.3  │
│  2. Step 1: ...               p.4  │
│  3. Step 2: ...               p.5  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│    SAFETY INFORMATION               │
│  ⚠️ Safety note 1                   │
│  ⚠️ Safety note 2                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│    PROCEDURE                        │
│                                     │
│  Step 1                            │
│  Pick up the 5mm wrench...         │
│  [IMAGE: Screenshot at 12.5s]      │
│  Note: This tool is required...    │
│                                     │
│  Step 2                            │
│  Insert bolt into hole...          │
│  [IMAGE: Screenshot at 25.0s]      │
│  Note: Ensure proper alignment...  │
└─────────────────────────────────────┘
```

---

## 🚀 Usage Patterns

### Basic Usage
```powershell
python main.py video.mp4
```

### Production Usage
```powershell
python main.py manufacturing_video.mp4 `
  --output "Assembly_SOP_v1.0.pdf" `
  --context "PCB assembly line procedure" `
  --company "TechManufacturing Inc"
```

### Batch Processing
```powershell
# Process multiple videos
python main.py video1.mp4 -o sop1.pdf
python main.py video2.mp4 -o sop2.pdf
python main.py video3.mp4 -o sop3.pdf
```

### Quick Testing
```powershell
# Use direct mode for speed
python main.py test_video.mp4 --direct-video
```

---

## 🎯 Success Indicators

### System is Working When:
✅ All imports successful (no errors)
✅ API key connects to Gemini
✅ Video frames extract correctly
✅ AI returns structured JSON
✅ PDF generates with images
✅ Output is professional quality

### Quality Checks:
✅ Steps are in logical order
✅ Instructions are clear and actionable
✅ Images match the steps
✅ Timestamps are accurate
✅ Safety notes are relevant
✅ Professional formatting

---

## 📈 Optimization Tips

### Speed
- Use `--direct-video` for faster processing
- Increase `interval_seconds` to extract fewer frames
- Use shorter test videos initially

### Quality
- Use frame extraction mode (default)
- Provide detailed context
- Use high-quality source videos
- Review and edit output

### Cost
- Monitor API usage
- Use free tier for testing
- Batch process during off-peak hours
- Cache results when possible

---

## 🔧 Customization Points

### Easy (No coding)
1. Adjust command-line arguments
2. Change context descriptions
3. Modify company names
4. Use different videos

### Medium (Basic Python)
1. Edit frame extraction interval
2. Change PDF colors/fonts
3. Modify AI temperature
4. Adjust image sizes

### Advanced (Experienced)
1. Add new AI prompts
2. Custom PDF layouts
3. Multi-language support
4. Web interface integration

---

## 📞 Quick Reference

### Key Commands
```powershell
# Test installation
python demo.py

# Generate SOP (basic)
python main.py video.mp4

# Generate SOP (full options)
python main.py video.mp4 -o output.pdf -c "context" --company "Name"

# Check packages
pip list

# Reinstall dependencies
pip install -r requirements.txt
```

### Key Files to Edit
- `.env` - API keys
- `video_processor.py` - Frame settings
- `sop_analyzer.py` - AI prompts
- `pdf_generator.py` - PDF styling

---

## 🎓 Understanding the Code

### Start Here (Easiest)
1. `main.py` - See overall flow
2. `demo.py` - See testing examples

### Then Read (Important)
3. `video_processor.py` - Video handling
4. `sop_analyzer.py` - AI integration

### Finally (Advanced)
5. `pdf_generator.py` - Document creation

---

**You now have a complete understanding of the Video-to-SOP Generator!** 🎉

Next step: **Set up your API key and test it!**

```powershell
python demo.py
```
