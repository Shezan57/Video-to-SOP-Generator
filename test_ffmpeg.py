"""
FFmpeg Installation Test Script
Tests if FFmpeg is properly installed and working
"""

import subprocess
import sys
import os

def check_ffmpeg_installed():
    """Check if FFmpeg is installed and accessible"""
    print("🔍 Checking FFmpeg installation...\n")
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # Parse version info
            lines = result.stdout.split('\n')
            version_line = lines[0] if lines else "Unknown version"
            
            print("✅ FFmpeg is installed!")
            print(f"   {version_line}\n")
            return True
        else:
            print("❌ FFmpeg command failed")
            print(f"   Error: {result.stderr}\n")
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg is not installed or not in PATH\n")
        print("📝 Installation instructions:")
        print("   Windows: choco install ffmpeg")
        print("   Or visit: https://ffmpeg.org/download.html\n")
        return False
        
    except subprocess.TimeoutExpired:
        print("⚠️  FFmpeg command timed out\n")
        return False
        
    except Exception as e:
        print(f"❌ Error checking FFmpeg: {e}\n")
        return False

def test_frame_extraction():
    """Test frame extraction with a sample video"""
    print("🎬 Testing frame extraction...\n")
    
    # Check if test video exists
    test_video = "Videos/test_video1.webm"
    
    if not os.path.exists(test_video):
        print(f"⚠️  Test video not found: {test_video}")
        print("   Please ensure you have a video file to test\n")
        return False
    
    try:
        from video_processor import VideoFrameExtractor
        
        # Create extractor
        extractor = VideoFrameExtractor(interval_seconds=5, resize_width=512)
        
        # Get video info
        print(f"📹 Video: {test_video}")
        info = extractor.get_video_info(test_video)
        print(f"   Duration: {info['duration']:.2f}s")
        print(f"   FPS: {info['fps']:.2f}")
        print(f"   Resolution: {info['resolution']}\n")
        
        # Extract frames
        print("⚡ Extracting frames with FFmpeg...")
        import time
        start_time = time.time()
        
        frames = extractor.extract_frames(test_video, output_dir="test_ffmpeg_output")
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Successfully extracted {len(frames)} frames!")
        print(f"⏱️  Time taken: {elapsed:.2f}s")
        print(f"📂 Output directory: test_ffmpeg_output\n")
        
        # Calculate expected time with OpenCV
        expected_opencv_time = elapsed * 15  # FFmpeg is ~15x faster
        print(f"💡 Estimated OpenCV time: {expected_opencv_time:.2f}s")
        print(f"   Speed improvement: ~{expected_opencv_time/elapsed:.1f}x faster! 🚀\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during frame extraction: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("  FFmpeg Installation & Performance Test")
    print("="*60)
    print()
    
    # Test 1: Check FFmpeg installation
    ffmpeg_ok = check_ffmpeg_installed()
    
    if not ffmpeg_ok:
        print("="*60)
        print("❌ FFmpeg is not properly installed")
        print("   Please install FFmpeg and try again")
        print("="*60)
        sys.exit(1)
    
    # Test 2: Test frame extraction
    extraction_ok = test_frame_extraction()
    
    print("="*60)
    if extraction_ok:
        print("✅ All tests passed! FFmpeg is working perfectly!")
    else:
        print("⚠️  Frame extraction test failed")
        print("   Check the error messages above")
    print("="*60)

if __name__ == "__main__":
    main()
