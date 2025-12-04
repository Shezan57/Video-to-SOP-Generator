# Video-to-SOP Generator - Code Structure

## 📁 Project Structure

```
Video-to-SOP Generator/
├── main.py                      # Main application entry point
├── video_processor.py           # Video frame extraction
├── sop_analyzer.py             # AI analysis with Gemini 2.5 Pro
├── pdf_generator.py            # PDF document generation
├── whisper_transcription.py    # Audio transcription via Whisper/Groq
├── test_pdf_generation.py      # Test script
├── requirements.txt            # Python dependencies
├── .env                        # API keys (not in git)
├── .env.example               # Example environment file
├── README.md                   # Main documentation
├── QUICKSTART.md              # Quick start guide
└── Videos/                     # Input video folder
    └── test_video1.webm       # Sample test video
```

## 🔧 Core Modules

### 1. **main.py**
**Purpose:** Orchestrates the entire SOP generation pipeline

**Key Components:**
- `VideoToSOPGenerator` class
- `generate_sop()` method - coordinates all steps
- Command-line interface with argparse

**Flow:**
1. Validate input video
2. Extract audio transcript (Whisper)
3. Extract video frames (OpenCV)
4. Analyze frames with AI (Gemini)
5. Generate PDF document

**Usage:**
```bash
python main.py "path/to/video.mp4" -o "output.pdf" -c "Context" --company "Company Name"
```

---

### 2. **video_processor.py**
**Purpose:** Extract frames from video files for AI analysis

**Key Components:**
- `VideoFrameExtractor` class
- `extract_frames()` - Extract frames at regular intervals
- `get_video_info()` - Get video metadata
- `extract_frame_at_timestamp()` - Extract specific frame

**Parameters:**
- `interval_seconds`: Frame extraction interval (default: 2 seconds)

**Output:**
- List of dictionaries with `timestamp` and `image_data` (base64)

---

### 3. **sop_analyzer.py**
**Purpose:** AI-powered video analysis using Gemini 2.5 Pro

**Key Components:**
- `SOPAnalyzer` class
- `analyze_video_frames()` - Main analysis method
- `_create_prompt()` - Build AI prompt with context
- `_parse_response()` - Parse JSON response

**AI Model:** `gemini-2.5-pro`

**Input:**
- Video frames (images)
- Audio transcript (optional)
- Task context (optional)

**Output JSON Structure:**
```json
{
  "title": "Task Name",
  "description": "Overview",
  "safety_notes": ["Note 1", "Note 2"],
  "steps": [
    {
      "step_number": 1,
      "instruction": "Action to perform",
      "timestamp_seconds": 12.5,
      "reasoning": "Why this matters"
    }
  ]
}
```

---

### 4. **pdf_generator.py**
**Purpose:** Create professional SOP PDF documents

**Key Components:**
- `SOPPDFGenerator` class
- `generate_sop_pdf()` - Main PDF generation
- Custom paragraph styles (title, headers, body)
- Image embedding from extracted frames

**PDF Structure:**
1. Title page (company name, title, metadata)
2. Table of contents
3. Safety information (if present)
4. Procedure steps with images

**Features:**
- Professional styling with custom colors
- Embedded images at specific timestamps
- Automatic image cleanup (temporary files)
- Page breaks for readability

---

### 5. **whisper_transcription.py**
**Purpose:** Audio extraction and transcription using Whisper

**Key Components:**
- `extract_audio_from_video()` - Extract audio track
- `transcribe_with_whisper_groq()` - Transcribe using Groq API
- `transcribe_video_audio()` - Complete pipeline

**API:** Groq (Whisper Large V3 model)

**Process:**
1. Extract audio with ffmpeg → MP3
2. Send to Groq Whisper API
3. Clean up temporary audio file

---

### 6. **test_pdf_generation.py**
**Purpose:** Automated testing script

**Features:**
- API key validation
- Complete pipeline test
- File size reporting
- Error handling and traceback

**Usage:**
```bash
python test_pdf_generation.py
```

---

## 🔑 Environment Variables

Required in `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

---

## 📦 Dependencies

**Core:**
- `opencv-python` - Video frame extraction
- `google-generativeai` - Gemini AI API
- `reportlab` - PDF generation
- `groq` - Whisper transcription API

**Supporting:**
- `python-dotenv` - Environment variables
- `Pillow` - Image processing
- `numpy` - Numerical operations
- `imageio-ffmpeg` - Audio extraction

See `requirements.txt` for complete list with versions.

---

## 🔄 Data Flow

```
Video File (.mp4, .webm, etc.)
    │
    ├─→ Audio Extraction (ffmpeg)
    │       └─→ Whisper API (Groq)
    │               └─→ Text Transcript
    │
    ├─→ Frame Extraction (OpenCV)
    │       └─→ Images (base64)
    │
    └─→ AI Analysis (Gemini 2.5 Pro)
            └─→ SOP JSON Structure
                    └─→ PDF Generation (ReportLab)
                            └─→ Final SOP Document
```

---

## 🎯 Key Design Decisions

1. **Frame-based approach:** Extract frames instead of direct video upload for better control and image quality in PDF

2. **Base64 encoding:** Keep frames in memory to avoid excessive file I/O

3. **Temporary file cleanup:** Use try-finally to ensure cleanup even on errors

4. **Modular design:** Each module has single responsibility for maintainability

5. **Gemini 2.5 Pro:** Latest stable model for best quality analysis

6. **Groq Whisper:** Fast, accurate audio transcription

---

## 🧪 Testing

Run the test script:
```bash
python test_pdf_generation.py
```

Expected output:
- ✓ API keys validated
- ✓ Audio transcribed (~2,500 characters)
- ✓ 120 frames extracted (for 240s video)
- ✓ 6-8 steps generated
- ✓ PDF created (~400-500 KB)

---

## 🚀 Performance Notes

**Typical processing time** (for 4-minute video):
- Audio extraction: ~5 seconds
- Whisper transcription: ~10 seconds
- Frame extraction: ~15 seconds
- AI analysis: ~30-60 seconds (depends on API)
- PDF generation: ~5 seconds

**Total:** ~1-2 minutes

---

## 📝 Code Quality

- **Type hints:** Used throughout for clarity
- **Docstrings:** All classes and methods documented
- **Error handling:** Comprehensive try-except blocks
- **Clean imports:** Only necessary imports
- **No dead code:** Unused functions removed

---

## 🔒 Security

- API keys stored in `.env` (not committed to git)
- `.env.example` provided for reference
- Temporary files cleaned up automatically
- No sensitive data in logs

---

## 📚 Documentation Files

- `README.md` - Complete project overview
- `QUICKSTART.md` - Quick start guide
- `CODE_STRUCTURE.md` - This file (architecture)
- `AUDIO_FEATURE.md` - Audio transcription details
- `PROJECT_SUMMARY.md` - Project summary

---

*Last updated: December 1, 2025*
