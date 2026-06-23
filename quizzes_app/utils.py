import json
import os
import tempfile
import subprocess
from django.core.exceptions import ValidationError
import yt_dlp
import whisper

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