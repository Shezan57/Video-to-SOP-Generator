# Video Files and Git

## ⚠️ Important: Do NOT Commit Video Files

Video files are **automatically ignored** by git to prevent issues with GitHub's file size limits.

### Why Video Files Are Ignored

- GitHub has a **100 MB file size limit**
- Video files are typically **very large** (100-500+ MB)
- They cause push failures and bloat the repository
- Test videos should be stored locally only

### .gitignore Configuration

The following video formats are ignored:
```
*.mp4
*.avi
*.mov
*.webm
*.mkv
```

### Where to Store Video Files

✅ **Local Storage:**
```
Video-to-SOP-Generator/
  Videos/
    test_video1.webm          ← Stored locally, not in git
    repair_tutorial.mp4        ← Stored locally, not in git
    training_video.mov         ← Stored locally, not in git
```

✅ **For Testing:**
- Keep your test videos in the `Videos/` folder
- They will work fine locally
- They won't be committed to git

✅ **For Sharing:**
- Use cloud storage (Google Drive, Dropbox, OneDrive)
- Share download links in documentation
- Use Git LFS for repositories that require video storage

### Sample Videos

If you need sample videos for testing:
1. Download from: https://www.pexels.com/videos/ (free videos)
2. Place in `Videos/` folder
3. Use in your commands:
   ```bash
   python main.py "Videos/your_video.mp4"
   ```

### If You Accidentally Committed a Large File

If you get an error like:
```
error: File Videos/large_video.webm is 142.08 MB; 
this exceeds GitHub's file size limit of 100.00 MB
```

**Solution:**
1. Unstage the file:
   ```bash
   git restore --staged Videos/large_video.webm
   ```

2. Make sure .gitignore includes `*.webm`

3. Commit without the video:
   ```bash
   git commit -m "Your commit message"
   ```

4. Push again:
   ```bash
   git push origin main
   ```

---

## Summary

✅ Videos work locally  
✅ Videos are ignored by git  
✅ No large files in repository  
✅ Fast cloning and pushing  

Keep your videos local, and your repository will stay clean and fast! 🚀
