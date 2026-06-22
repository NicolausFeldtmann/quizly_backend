import json
import os
import tempfile
from django.core.exceptions import ValidationError

def exract_youtube_info(url):

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "no_warnings": True
    }

    try:
        with yt_dlp.YouTubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, downloaded=False)

            return {
                "title": info.get("title", ""),
                "description": info.get("description", "")
            }
    except Exception as e:
        raise ValidationError(f"Error whihle extract information from YouTube: {str(e)}")