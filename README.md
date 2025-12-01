# Video-to-SOP Generator

Convert training videos into professional Standard Operating Procedure (SOP) manuals automatically using AI.

## Overview

This tool uses multimodal AI (Gemini 1.5 Pro) to watch industrial/manufacturing training videos and generate step-by-step instruction manuals with screenshots.

## Features

- 🎥 **Video Processing**: Extracts key frames from training videos using FFmpeg (15x faster!)
- 🎙️ **Audio Transcription**: High-quality speech-to-text using Whisper AI
- 🤖 **AI Analysis**: Uses Gemini 1.5 Flash to understand and document procedures
- 📄 **PDF Generation**: Creates professional SOP manuals with images
- ⚡ **Fast Processing**: FFmpeg-powered frame extraction for optimal performance
- 🔒 **Safety Notes**: Automatically identifies safety considerations

## Installation

### Prerequisites

- Python 3.8+
- FFmpeg ([Installation guide](FFMPEG_SETUP.md))
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Groq API key for Whisper transcription ([Get one here](https://console.groq.com/))

### Setup

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv myvenv
   .\myvenv\Scripts\activate  # Windows
   source myvenv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**:
   - Copy `.env.example` to `.env`
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

## Usage

### Basic Usage

```bash
python main.py path/to/video.mp4
```

This will:
1. Process the video
2. Analyze it with AI
3. Generate `output_sop.pdf`

### Advanced Usage

```bash
python main.py video.mp4 \
  --output my_sop.pdf \
  --context "Engine valve assembly process" \
  --company "ACME Manufacturing" \
  --direct-video
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `video` | Path to input video file | (required) |
| `-o, --output` | Output PDF filename | `output_sop.pdf` |
| `-c, --context` | Task context for better analysis | Auto-detected |
| `--company` | Company name for PDF header | "Your Company" |
| `--direct-video` | Upload video directly to Gemini | Frame extraction |

## How It Works

### Pipeline

```
Video Input → Frame Extraction → AI Analysis → PDF Generation
```

### 1. Video Processing (`video_processor.py`)
- Extracts frames at 1-2 second intervals
- Resizes images for optimal AI processing
- Maintains timestamp information

### 2. AI Analysis (`sop_analyzer.py`)
- Sends frames/video to Gemini 1.5 Pro
- Uses specialized prompt for SOP generation
- Returns structured JSON with steps and timestamps

### 3. PDF Generation (`pdf_generator.py`)
- Creates professional document layout
- Embeds images at relevant steps
- Includes safety notes and table of contents

## Project Structure

```
Video-to-SOP Generator/
├── main.py                 # Main application
├── video_processor.py      # Frame extraction
├── sop_analyzer.py        # AI analysis
├── pdf_generator.py       # PDF creation
├── requirements.txt       # Dependencies
├── .env.example          # API key template
└── README.md             # This file
```

## Example Output

The generated PDF includes:

- **Title Page**: Task name, description, document info
- **Table of Contents**: Quick navigation
- **Safety Section**: Important safety considerations
- **Procedure Steps**: Step-by-step instructions with:
  - Clear numbered steps
  - Action-oriented instructions
  - Screenshot at each step
  - Timestamp reference
  - Additional notes/reasoning

## Configuration

### Frame Extraction Settings

Edit `video_processor.py`:
```python
extractor = VideoFrameExtractor(
    interval_seconds=2,    # Extract 1 frame every 2 seconds
    resize_width=512      # Resize width (maintains aspect ratio)
)
```

### AI Model Settings

Edit `sop_analyzer.py`:
```python
generation_config={
    "temperature": 0.4,        # Lower = more consistent
    "max_output_tokens": 8192  # Maximum response length
}
```

## Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure you created `.env` file (not `.env.example`)
- Verify the API key is valid

### "Import cv2 could not be resolved"
- Install OpenCV: `pip install opencv-python`

### Video processing fails
- Check video format (MP4, MOV supported)
- Ensure video file is not corrupted
- Try with a shorter video first

### PDF generation fails
- Install ReportLab: `pip install reportlab`
- Check disk space for output file

## Business Applications

### Target Customers
- Manufacturing companies
- Industrial training departments
- Safety compliance teams
- Equipment vendors
- Consulting firms

### Pricing Model Ideas
1. **Per-video pricing**: $50-200 per video
2. **SaaS subscription**: $99-499/month
3. **Enterprise license**: Custom pricing
4. **API access**: Pay per API call

### Value Proposition
- Saves 10+ hours per manual
- Ensures consistency
- Easy updates when procedures change
- Reduces training time
- Improves compliance

## Limitations

- Video quality affects AI accuracy
- Works best with clear, well-lit videos
- Requires stable camera angle
- English language optimized (can be adapted)
- Processing time depends on video length

## Future Enhancements

- [ ] Web interface (Flask/Django)
- [ ] Multi-language support
- [ ] Video quality validation
- [ ] Custom branding options
- [ ] Step editing interface
- [ ] Voice narration in video
- [ ] Multiple video formats
- [ ] Batch processing

## Dependencies

- `opencv-python`: Video frame extraction
- `google-generativeai`: Gemini AI API
- `reportlab`: PDF generation
- `Pillow`: Image processing
- `python-dotenv`: Environment configuration

## License

This project is for educational and commercial use.

## Support

For questions or issues, please check:
1. This README
2. Code comments in source files
3. API documentation

## Credits

Built with:
- Google Gemini 1.5 Pro
- OpenCV
- ReportLab

---

**Made for industrial training excellence** 🏭
