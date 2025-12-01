"""
Video Frame Extractor Module
Extracts frames from video files at specified intervals
"""

import cv2
import base64
import os
import subprocess
import tempfile
from typing import List, Dict
from pathlib import Path


class VideoFrameExtractor:
    """Extract frames from video files for SOP generation"""
    
    def __init__(self, interval_seconds: int = 1, resize_width: int = 512):
        """
        Initialize the frame extractor
        
        Args:
            interval_seconds: Extract one frame every N seconds
            resize_width: Resize frame width (maintains aspect ratio)
        """
        self.interval_seconds = interval_seconds
        self.resize_width = resize_width
    
    def extract_frames(self, video_path: str, output_dir: str = None) -> List[Dict]:
        """
        Extract frames from video at specified intervals using FFmpeg
        
        Args:
            video_path: Path to the video file
            output_dir: Directory to save extracted frames (optional)
            
        Returns:
            List of dictionaries containing frame info:
            [
                {
                    "id": frame_number,
                    "timestamp": seconds,
                    "image_path": path_to_saved_image,
                    "image_data": base64_encoded_image
                }
            ]
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Get video info first
        info = self.get_video_info(video_path)
        duration = info['duration']
        
        print(f"Video Info: {duration:.2f}s, {info['fps']:.2f} FPS, {info['total_frames']} frames")
        print(f"Extracting 1 frame every {self.interval_seconds} seconds using FFmpeg...")
        
        # Create output directory or use temp directory
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            temp_dir = output_dir
            cleanup_temp = False
        else:
            temp_dir = tempfile.mkdtemp()
            cleanup_temp = True
        
        try:
            # Build FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f'fps=1/{self.interval_seconds},scale={self.resize_width}:-1',
                '-q:v', '2',  # High quality JPEG
                '-threads', '0',  # Auto-detect optimal thread count
                '-loglevel', 'error',  # Only show errors
                f'{temp_dir}/frame_%06d.jpg'
            ]
            
            # Execute FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"FFmpeg error: {result.stderr}")
            
            # Load extracted frames
            frames = []
            frame_files = sorted(Path(temp_dir).glob('frame_*.jpg'))
            
            if not frame_files:
                raise Exception("No frames were extracted. Check if FFmpeg is installed correctly.")
            
            for img_file in frame_files:
                # Extract frame number from filename (frame_000001.jpg -> 1)
                frame_num = int(img_file.stem.split('_')[1])
                timestamp = (frame_num - 1) * self.interval_seconds
                
                # Read and encode to base64
                with open(img_file, 'rb') as f:
                    image_bytes = f.read()
                    base64_image = base64.b64encode(image_bytes).decode('utf-8')
                
                frame_info = {
                    "id": frame_num,
                    "timestamp": timestamp,
                    "image_data": base64_image
                }
                
                # Add image path if saving permanently
                if output_dir:
                    frame_info["image_path"] = str(img_file)
                
                frames.append(frame_info)
                print(f"Loaded frame {len(frames)} at {timestamp:.2f}s")
            
            print(f"Total frames extracted: {len(frames)}")
            return frames
            
        finally:
            # Clean up temp directory if created
            if cleanup_temp and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
    
    def extract_frames_opencv(self, video_path: str, output_dir: str = None) -> List[Dict]:
        """
        Legacy OpenCV method for frame extraction (slower but no FFmpeg dependency)
        
        Args:
            video_path: Path to the video file
            output_dir: Directory to save extracted frames (optional)
            
        Returns:
            List of dictionaries containing frame info
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Create output directory if specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        print(f"Video Info: {duration:.2f}s, {fps:.2f} FPS, {total_frames} frames")
        print(f"Extracting 1 frame every {self.interval_seconds} seconds...")
        
        frames = []
        count = 0
        frame_interval = int(fps * self.interval_seconds)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Extract frame at specified interval
            if count % frame_interval == 0:
                timestamp = count / fps
                
                # Resize frame
                resized_frame = self._resize_frame(frame)
                
                # Encode to JPEG
                _, buffer = cv2.imencode('.jpg', resized_frame)
                base64_image = base64.b64encode(buffer).decode('utf-8')
                
                frame_info = {
                    "id": count,
                    "timestamp": timestamp,
                    "image_data": base64_image
                }
                
                # Save to disk if output_dir specified
                if output_dir:
                    frame_filename = f"frame_{count:06d}.jpg"
                    frame_path = os.path.join(output_dir, frame_filename)
                    cv2.imwrite(frame_path, resized_frame)
                    frame_info["image_path"] = frame_path
                
                frames.append(frame_info)
                print(f"Extracted frame {len(frames)} at {timestamp:.2f}s")
            
            count += 1
        
        cap.release()
        print(f"Total frames extracted: {len(frames)}")
        
        return frames
    
    def _resize_frame(self, frame):
        """Resize frame while maintaining aspect ratio"""
        height, width = frame.shape[:2]
        
        if width > self.resize_width:
            # Calculate new height to maintain aspect ratio
            ratio = self.resize_width / width
            new_height = int(height * ratio)
            resized = cv2.resize(frame, (self.resize_width, new_height))
            return resized
        
        return frame
    
    def get_video_info(self, video_path: str) -> Dict:
        """Get video metadata"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps if fps > 0 else 0
        
        cap.release()
        
        return {
            "duration": duration,
            "fps": fps,
            "total_frames": total_frames,
            "width": width,
            "height": height,
            "resolution": f"{width}x{height}"
        }
    
    def extract_frame_at_timestamp(self, video_path: str, timestamp: float) -> bytes:
        """
        Extract a single frame at a specific timestamp
        
        Args:
            video_path: Path to video file
            timestamp: Time in seconds
            
        Returns:
            JPEG image as bytes
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Set position to timestamp
        frame_number = int(timestamp * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise ValueError(f"Could not extract frame at {timestamp}s")
        
        # Encode to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()


if __name__ == "__main__":
    # Test the extractor
    extractor = VideoFrameExtractor(interval_seconds=2)
    
    # Example usage
    video_path = "sample_video.mp4"
    if os.path.exists(video_path):
        info = extractor.get_video_info(video_path)
        print("Video Info:", info)
        
        frames = extractor.extract_frames(video_path, output_dir="extracted_frames")
        print(f"Extracted {len(frames)} frames")
