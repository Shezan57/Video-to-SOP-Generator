"""
AI Analyzer Module
Uses Gemini 2.5 Pro to analyze video frames and generate SOP steps
"""

import os
import json
import io
import base64
from typing import List, Dict, Optional
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()


class SOPAnalyzer:
    """Analyze video frames and generate Standard Operating Procedures"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the SOP Analyzer
        
        Args:
            api_key: Google API key (if not provided, reads from .env)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in .env file")
        
        # Configure Google API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
    
    def analyze_video_frames(self, frames: List[Dict], context: str = "", audio_transcript: str = "") -> Dict:
        """
        Analyze video frames and generate SOP
        
        Args:
            frames: List of frame dictionaries with 'image_data' and 'timestamp'
            context: Optional context about the task (e.g., "Engine assembly process")
            audio_transcript: Optional audio transcript from the video
            
        Returns:
            Dictionary containing SOP structure with title, description, and steps
        """
        print("Preparing prompt for Gemini...")
        
        # Create the prompt
        prompt = self._create_prompt(frames, context, audio_transcript)
        
        # Prepare content for Gemini (text + images)
        content_parts = [prompt]
        
        # Add images to the content
        for frame in frames:
            # Decode base64 image data and create PIL Image
            image_bytes = base64.b64decode(frame['image_data'])
            image = Image.open(io.BytesIO(image_bytes))
            content_parts.append(image)
        
        print(f"Sending {len(frames)} frames to Gemini for analysis...")
        
        try:
            # Generate content
            response = self.model.generate_content(
                content_parts,
                generation_config={
                    "temperature": 0.4,
                    "top_p": 0.95,
                    "max_output_tokens": 8192,
                }
            )
            
            # Extract JSON from response
            response_text = response.text
            print("Received response from Gemini")
            
            # Parse JSON
            sop_data = self._parse_response(response_text)
            
            return sop_data
            
        except Exception as e:
            print(f"Error during Gemini analysis: {e}")
            raise
    
    def _create_prompt(self, frames: List[Dict], context: str, audio_transcript: str = "") -> str:
        """Create the system prompt for Gemini"""
        
        # Create timestamp information
        timestamps = [f"Frame {i+1} at {frame['timestamp']:.2f}s" 
                     for i, frame in enumerate(frames)]
        timestamp_info = "\n".join(timestamps)
        
        # Add audio transcript section if available
        audio_section = ""
        if audio_transcript:
            audio_section = f"""

Audio Transcript:
{audio_transcript}

Use the audio transcript to better understand what is being said or explained during the procedure. The spoken words provide important context about the actions being performed.
"""
        
        prompt = f"""You are an expert Technical Writer specializing in Standard Operating Procedures (SOPs) for industrial and manufacturing processes.

Task Context: {context if context else "Manufacturing/assembly process"}

You will receive a sequence of {len(frames)} frames from a video showing a worker performing a task. 

Frame Timestamps:
{timestamp_info}
{audio_section}

Your job is to:
1. Watch the sequence carefully
2. Listen to the audio transcript (if provided) for additional context
3. Identify distinct actions/steps being performed (including disassembly AND reassembly)
4. Write clear, actionable instructions for each step
5. Select the best timestamp where each action is most clearly visible
6. Provide reasoning for why that step matters

CRITICAL INSTRUCTIONS FOR REPAIR/MAINTENANCE PROCEDURES:
- If the procedure involves disassembly (removing parts), YOU MUST include the reassembly steps
- After repair/replacement, include all steps to put components back together in REVERSE order
- Reference the disassembly steps when writing reassembly (e.g., "Reinstall the cover removed in Step 3")
- Include torque specifications, alignment checks, and final verification steps
- For each removed component, ensure there is a corresponding reinstallation step

Output Format (STRICT JSON):
{{
  "title": "Descriptive Task Name",
  "description": "Brief overview of the entire process (mention if it includes disassembly and reassembly)",
  "safety_notes": ["Safety consideration 1", "Safety consideration 2"],
  "steps": [
    {{
      "step_number": 1,
      "instruction": "Clear, imperative instruction (e.g., 'Pick up the 5mm Allen wrench')",
      "timestamp_seconds": 12.5,
      "reasoning": "Why this step is important or what to watch for"
    }}
  ]
}}

Important Guidelines:
- Each step must be atomic (one clear action)
- Use imperative voice ("Pick up", "Turn", "Connect", not "The worker picks up")
- Be specific about tools, parts, and measurements
- Include safety warnings if relevant
- Choose timestamps where the action is CLEAREST
- For repair procedures: Include BOTH disassembly steps AND reassembly steps
- For reassembly: Reference which parts are being reinstalled (e.g., "Reinstall the valve cover", "Reattach the bolts")
- Include final verification steps (e.g., "Test the repair", "Check for leaks", "Verify operation")
- Aim for 5-20 steps depending on complexity

Output ONLY valid JSON. Do not include any markdown formatting or code blocks.
"""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse the LLM response into structured JSON"""
        
        # Remove markdown code blocks if present
        text = response_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        text = text.strip()
        
        try:
            data = json.loads(text)
            
            # Validate structure
            if "title" not in data or "steps" not in data:
                raise ValueError("Response missing required fields: title or steps")
            
            # Ensure steps have required fields
            for step in data["steps"]:
                required_fields = ["step_number", "instruction", "timestamp_seconds"]
                for field in required_fields:
                    if field not in step:
                        raise ValueError(f"Step missing required field: {field}")
            
            return data
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Response text: {text[:500]}...")
            raise ValueError("LLM did not return valid JSON")