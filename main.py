"""
Video-to-SOP Generator
Main application file that orchestrates the entire pipeline
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

from video_processor import VideoFrameExtractor
from sop_analyzer import SOPAnalyzer
from pdf_generator import SOPPDFGenerator
from datetime import datetime

# Load environment variables
load_dotenv()


class VideoToSOPGenerator:
    """Main application class for Video-to-SOP generation"""
    
    def __init__(self):
        """Initialize the generator"""
        self.video_processor = VideoFrameExtractor(interval_seconds=2)
        self.analyzer = SOPAnalyzer()
        self.pdf_generator = SOPPDFGenerator()
    
    def generate_sop(
        self,
        video_path: str,
        output_pdf: str,
        context: str = "",
        company_name: str = "Your Company"
    ):
        """
        Generate SOP from video file
        
        Args:
            video_path: Path to input video
            output_pdf: Path for output PDF
            context: Optional context about the task
            company_name: Company name for PDF header
        """
        
        # Validate input
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        print("=" * 60)
        print("VIDEO-TO-SOP GENERATOR")
        print("=" * 60)
        print(f"Input Video: {video_path}")
        print(f"Output PDF: {output_pdf}")
        print(f"Context: {context if context else 'Auto-detected'}")
        print("=" * 60)
        
        # Start total timing
        total_start_time = time.time()
        
        # Get video info
        video_info = self.video_processor.get_video_info(video_path)
        print(f"\nVideo Information:")
        print(f"  Duration: {video_info['duration']:.2f} seconds")
        print(f"  Resolution: {video_info['resolution']}")
        print(f"  FPS: {video_info['fps']:.2f}")
        
        # Step 1: Process video
        print("\n" + "=" * 60)
        print("STEP 1: VIDEO PROCESSING")
        print("=" * 60)
        
        # Step 1a: Extract audio transcript (using Whisper via Groq)
        audio_transcript = ""
        audio_start_time = time.time()
        try:
            from whisper_transcription import transcribe_video_audio
            groq_api_key = os.getenv("GROQ_API_KEY")
            if groq_api_key:
                audio_transcript = transcribe_video_audio(video_path, groq_api_key) or ""
                if audio_transcript:
                    audio_elapsed = time.time() - audio_start_time
                    print(f"✓ Audio transcript extracted: {len(audio_transcript)} characters")
                    print(f"  Time: {int(audio_elapsed // 60)}m {int(audio_elapsed % 60)}s")
            else:
                print("⚠️  GROQ_API_KEY not found, skipping audio transcription")
        except Exception as e:
            print(f"⚠️  Audio transcription skipped: {e}")
        
        # Initialize frames
        frames = []
        
        print("\nExtracting frames from video...")
        
        # Create temp directory for frames
        frames_dir = "extracted_frames"
        os.makedirs(frames_dir, exist_ok=True)
        
        # Time frame extraction
        frame_start_time = time.time()
        frames = self.video_processor.extract_frames(
            video_path,
            output_dir=frames_dir
        )
        frame_elapsed = time.time() - frame_start_time
        
        print(f"\n✓ Extracted {len(frames)} frames")
        print(f"  Time: {int(frame_elapsed // 60)}m {int(frame_elapsed % 60)}s")
        
        # Step 2: Analyze with AI
        print("\n" + "=" * 60)
        print("STEP 2: AI ANALYSIS (with Audio Transcript)")
        print("=" * 60)
        analysis_start_time = time.time()
        sop_data = self.analyzer.analyze_video_frames(frames, context, audio_transcript)
        analysis_elapsed = time.time() - analysis_start_time
        
        print(f"\n✓ Generated SOP: {sop_data['title']}")
        print(f"  Total steps: {len(sop_data['steps'])}")
        print(f"  Time: {int(analysis_elapsed // 60)}m {int(analysis_elapsed % 60)}s")

        # Step 3: Generate PDF
        print("\n" + "=" * 60)
        print("STEP 3: PDF GENERATION")
        print("=" * 60)
        
        pdf_start_time = time.time()
        # Pass the extracted frames to PDF generator
        self.pdf_generator.generate_sop_pdf(
            sop_data,
            frames,  # Pass frames instead of video_path
            output_pdf,
            company_name
        )
        pdf_elapsed = time.time() - pdf_start_time
        
        # Calculate total time
        total_elapsed = time.time() - total_start_time
        
        print("\n" + "=" * 60)
        print("COMPLETE!")
        print("=" * 60)
        print(f"SOP PDF saved to: {output_pdf}")
        print(f"Title: {sop_data['title']}")
        print(f"Steps: {len(sop_data['steps'])}")
        print("\n" + "=" * 60)
        print("TIMING SUMMARY")
        print("=" * 60)
        if audio_transcript:
            print(f"  Audio Transcription: {int(audio_elapsed // 60)}m {int(audio_elapsed % 60)}s")
        print(f"  Frame Extraction:    {int(frame_elapsed // 60)}m {int(frame_elapsed % 60)}s")
        print(f"  AI Analysis:         {int(analysis_elapsed // 60)}m {int(analysis_elapsed % 60)}s")
        print(f"  PDF Generation:      {int(pdf_elapsed // 60)}m {int(pdf_elapsed % 60)}s")
        print(f"  {'─' * 58}")
        print(f"  TOTAL TIME:          {int(total_elapsed // 60)}m {int(total_elapsed % 60)}s")
        print("=" * 60)
        
        return sop_data


def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Video-to-SOP Generator: Convert training videos to SOP manuals"
    )
    parser.add_argument(
        "video",
        help="Path to input video file"
    )
    parser.add_argument(
        "-o", "--output",
        default="output_sop.pdf",
        help="Output PDF filename (default: output_sop.pdf)"
    )
    parser.add_argument(
        "-c", "--context",
        default="",
        help="Context about the task (e.g., 'Engine assembly process')"
    )
    parser.add_argument(
        "--company",
        default="Your Company",
        help="Company name for PDF header"
    )
    
    args = parser.parse_args()
    
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY not found!")
        print("Please create a .env file with your API key:")
        print("  GOOGLE_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Create generator
    generator = VideoToSOPGenerator()
    
    try:
        # Generate SOP
        generator.generate_sop(
            video_path=args.video,
            output_pdf=args.output,
            context=args.context,
            company_name=args.company
        )
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
