# Quick Reference Card 📋

## One-Line Command

```powershell
python main.py "video.mp4" -o "output.pdf" -c "Task Description" --company "Company"
```

---

## Common Examples

### Car Repair
```powershell
python main.py "Videos\tire_repair.webm" -o "tire_repair_sop.pdf" -c "Flat Tire Repair" --company "Auto Shop"
```

### Equipment Maintenance
```powershell
python main.py "Videos\maintenance.mp4" -o "maintenance_sop.pdf" -c "Monthly Equipment Maintenance" --company "Factory"
```

### Manufacturing Process
```powershell
python main.py "Videos\assembly.mp4" -o "assembly_sop.pdf" -c "Product Assembly Process" --company "Manufacturing Inc"
```

---

## Command Options

| Short | Long | Description | Example |
|-------|------|-------------|---------|
| (required) | video file | Input video | `video.mp4` |
| `-o` | `--output` | Output PDF | `output.pdf` |
| `-c` | `--context` | Task description | `"Repair Process"` |
| | `--company` | Company name | `"Your Company"` |

---

## Processing Steps

1. 🎙️ **Audio** (~30s) - Extracts timestamped transcript
2. 🎬 **Frames** (~8s) - Extracts key frames with FFmpeg
3. 🤖 **AI** (~75s) - Analyzes and generates SOP
4. 📄 **PDF** (~5s) - Creates professional document
5. 🧹 **Cleanup** - Deletes temporary frames

**Total:** ~2 minutes for 4-minute video

---

## Output

```
repair_sop.pdf
├── Title page with company name
├── Overview and safety notes
├── Step-by-step instructions with images
└── Numbered steps with timestamps
```

---

## Requirements

- ✅ Python 3.8+
- ✅ FFmpeg installed
- ✅ `GOOGLE_API_KEY` in `.env`
- ✅ `GROQ_API_KEY` in `.env`

---

## Quick Setup

```powershell
# 1. Install packages
pip install -r requirements.txt

# 2. Install FFmpeg
choco install ffmpeg

# 3. Create .env file
echo GOOGLE_API_KEY=your_key > .env
echo GROQ_API_KEY=your_key >> .env

# 4. Run
python main.py "video.mp4"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| FFmpeg not found | `choco install ffmpeg` |
| API key missing | Add to `.env` file |
| Video too large | Keep under 10 minutes |
| Poor quality | Use 720p+ resolution |

---

## Performance

- Frame extraction: **15x faster** with FFmpeg
- 4-min video: ~2 minutes total
- 10-min video: ~5 minutes total

---

## Tips

✅ Clear audio narration  
✅ Good lighting  
✅ Stable camera  
✅ Specific context  
✅ Under 10 minutes  

---

## Help

- Full docs: `README.md`
- Setup guide: `QUICKSTART.md`
- FFmpeg help: `FFMPEG_SETUP.md`
- Changelog: `CHANGELOG.md`
- Complete summary: `FINAL_SUMMARY.md`

---

## Version

**v2.0.0** - December 2, 2025  
**Repository:** github.com/Shezan57/Video-to-SOP-Generator

---

**Quick Start:** Place video in `Videos/` folder → Run command → Get PDF! 🚀
