import json
import os
import tempfile
import subprocess
import shutil
from pathlib import Path
from django.core.exceptions import ValidationError
from google import genai
import yt_dlp
import whisper
import re
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

def extract_youtube_info(url):
    """Function to extract title, description and audio of YouTube clip."""
    """Sets format of audio and parameter to handle extraction."""

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "no_warnings": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            return {
                "title": info.get("title", ""),
                "description": info.get("description")
            }
    except Exception as e:
        raise ValidationError(f"Error extract informations from YouTube: {str(e)}")

def transcribe_yt_video(url):
    """Creats transcription text of extracted audio."""
    """Create temporary mp3 file for transcription."""
    """Deletes temporarry mp3 file regardless of whether errors accourred."""

    temp_dir = tempfile.mkdtemp()

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key":"FFmpegExtractAudio",
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
        raise ValidationError(f"Error transcibing video: {str(e)}")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def generate_quiz(transcript):
    """Generates quiz by using precise directions in prompt variable."""
    try:
        api_key = _get_api_key()
        client = genai.Client(api_key=api_key)
        prompt = _create_prompt(transcript)
        response = _call_gemini_api(client, prompt)
        response_text = _clean_response(response.text)
        quiz_data = _parse_json_response(response_text)
        _validate_quiz_structure(quiz_data)
        return quiz_data
    except Exception as e:
        print(f"General Error: {str(e)}")
        raise ValidationError(f"Error generating quiz: {str(e)}")


def _get_api_key():
    """Retrieves and validates the Google API key."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValidationError("GOOGLE_API_KEY is not configured in the .env file.")
    return api_key


def _create_prompt(transcript):
    """Creates the prompt for quiz generation."""
    return f"""
        Based on the following transcript, generate a quiz in valid JSON format.
        The quiz must follow this exact structure:
        {{
            "title": "Create a concise quiz title based on the topic of the transcript.",
            "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",
            "questions": [
                {{
                    "question_title": "The question goes here.",
                    "question_options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "the correct answer from the above options"
                }},
                ...
                (exactly 10 questions)
            ]
        }}
        Requirements:
        - Each question must have exactly 4 distinct answer options.
        - Only one correct answer is allowed per question, and it must be present in 'question_options'.
        - The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).
        - Do not include explanations, comments, or any text outside the JSON.
        - Do not wrap the JSON in markdown code blocks or backticks.
        - Return ONLY the raw JSON object, nothing else.

        TRANSCRIPT:
        {transcript}
    """


def _call_gemini_api(client, prompt):
    """Calls the Gemini API with the given prompt."""
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )


def _clean_response(response_text):
    """Cleans the API response by removing markdown code blocks."""
    response_text = response_text.strip()
    
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    elif response_text.startswith("```"):
        response_text = response_text[3:]
    
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    
    response_text = response_text.strip()
    
    print("Cleaned API Response:")
    print(response_text[:500])
    
    return response_text


def _parse_json_response(response_text):
    """Parses the JSON response from the API."""
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")
        print(f"Response text: {response_text[:1000]}")
        raise ValidationError(f"Error parsing quiz JSON: {str(e)}")


def _validate_quiz_structure(quiz_data):
    """Validates that the quiz has the required structure."""
    required_keys = ['title', 'description', 'questions']
    if not all(key in quiz_data for key in required_keys):
        raise ValidationError("Invalid quiz structure returned from API")


def normalize_yt_url(url):
    video_id_pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)'
    match = re.search(video_id_pattern, url)
    if not match:
        raise ValidationError("Invalid YouTube url")
    video_id = match.group(1)
    return f"https://www.youtube.com/watch?v={video_id}"
    
