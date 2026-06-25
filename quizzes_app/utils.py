import json
import os
import tempfile
import subprocess
from django.core.exceptions import ValidationError
from google import genai
import yt_dlp
import whisper
from dotenv import load_dotenv

load_dotenv()

def extract_youtube_info(url):

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "no_warnigs": True
    }

    try:
        with yt_dlp.YouTubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, downloaded=False)

            return {
                "title": info.get("title", ""),
                "description": info.get("description", "")
            }
    except Exception as e:
        raise ValidationError(f"Error extract informations from YouTube: {str(e)}")

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
    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

        prompt = f"""
            Based on the following transcript, generate a quiz in valid JSON format.
            The quiz must follow this exact structure:
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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        response_text = response.text.strip()

        if response_text.startswith("```json"):
            response_text = response_text[7:] 
        elif response_text.startswith("```"):
            response_text = response_text[3:] 
            
        if response_text.endswith("```"):
            response_text = response_text[:-3]  
        response_text = response_text.strip()
        
        print("Cleaned API Response:")
        print(response_text[:500])  
        
        quiz_data = json.loads(response_text)
        
        if 'title' not in quiz_data or 'description' not in quiz_data or 'questions' not in quiz_data:
            raise ValidationError("Invalid quiz structure returned from API")
        
        return quiz_data

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")
        print(f"Response text: {response_text[:1000]}") 
        raise ValidationError(f"Error parsing quiz JSON: {str(e)}")
    except Exception as e:
        print(f"General Error: {str(e)}")
        raise ValidationError(f"Error generating quiz: {str(e)}")
