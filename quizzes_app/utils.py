import json
import os
import tempfile
import subprocess
from django.core.exceptions import ValidationError
from google import genai
import yt_dlp
import whisper
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def extract_youtube_info(url):

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "no_warnings": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, downloaded=False)

            return {
                "title": info.get("title", ""),
                "description": info.get("description", ""),
            }
    except Exception as e:
        raise ValidationError(f"Error extract iformations from YouTube: {str(e)}")

def transcribe_yt_video(url):

    temp_dir = tempfile.mkdtemp()

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }],
            "outtmpl": os.path.join(temp_dir, "audio"),
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        audio_file = os.path.join(temp_dir, "audio.mp3")
        if not os.path.exists(audio_file):
            raise ValidationError("Failed to extract audio.")

        model = whisper.load_model("base")
        result = model.transcribe(audio_file, language="de")

        return result["text"]

    except Exception as e:
        raise ValidationError(f"Error transcribing video: {str(e)}")

    finally:
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def generate_quiz(transcript):
    """
    Generates a quiz in JSON format from a given transcript using Google Gemini API.
    
    Args:
        transcript (str): The transcript text to generate the quiz from
        
    Returns:
        dict: Parsed JSON quiz with structure containing title, description, and questions
        
    Raises:
        ValidationError: If API call fails or response is not valid JSON
    """
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValidationError("GOOGLE_API_KEY environment variable is not set")
        
        client = genai.Client(api_key=api_key)
        
        prompt = f"""Based on the following transcript, generate a quiz in valid JSON format.

**The quiz must follow this exact structure:**

{{
  "title": "Create a concise quiz title based on the topic of the transcript.",
  "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",
  "questions": [
    {{
      "question_title": "The question goes here.",
      "question_options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The correct answer from the above options"
    }},
    ...
    (exactly 10 questions)
  ]
}}

**Requirements:**

- Each question must have exactly 4 distinct answer options.
- Only one correct answer is allowed per question, and it must be present in 'question_options'.
- The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).
- Do not include explanations, comments, or any text outside the JSON.

**Transcript:**

{transcript}"""
        
        interaction = client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt
        )
        
        response_text = interaction.output_text
        
        # Parse the JSON response
        quiz_data = json.loads(response_text)
        
        # Validate the quiz structure
        if not isinstance(quiz_data, dict):
            raise ValidationError("Quiz response is not a valid dictionary")
        
        required_fields = ["title", "description", "questions"]
        for field in required_fields:
            if field not in quiz_data:
                raise ValidationError(f"Missing required field: {field}")
        
        if not isinstance(quiz_data["questions"], list):
            raise ValidationError("'questions' field must be a list")
        
        if len(quiz_data["questions"]) != 10:
            raise ValidationError(f"Expected 10 questions, got {len(quiz_data['questions'])}")
        
        # Validate each question
        for idx, question in enumerate(quiz_data["questions"]):
            if not isinstance(question, dict):
                raise ValidationError(f"Question {idx + 1} is not a dictionary")
            
            question_fields = ["question_title", "question_options", "answer"]
            for field in question_fields:
                if field not in question:
                    raise ValidationError(f"Question {idx + 1} missing field: {field}")
            
            if not isinstance(question["question_options"], list):
                raise ValidationError(f"Question {idx + 1} options must be a list")
            
            if len(question["question_options"]) != 4:
                raise ValidationError(f"Question {idx + 1} must have exactly 4 options, got {len(question['question_options'])}")
            
            if question["answer"] not in question["question_options"]:
                raise ValidationError(f"Question {idx + 1} answer is not in the options list")
        
        return quiz_data
        
    except json.JSONDecodeError as e:
        raise ValidationError(f"Failed to parse quiz JSON response: {str(e)}")
    except Exception as e:
        raise ValidationError(f"Error generating quiz: {str(e)}")

