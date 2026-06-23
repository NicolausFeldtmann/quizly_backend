from rest_framework import serializers
from django.contrib.auth.models import User
from quizzes_app.models import QuizzModel, QuestionsModel
from quizzes_app.utils import extract_youtube_info, transcribe_yt_video

class QuizzSeriazlizer(serializers.ModelSerializer):
    url = serializers.URLField(write_only=True, required=False)
    video_url = serializers.URLField(required=False)

    class Meta:
        model = QuizzModel
        fields = ["id", "title", "description", "transcript", "created_at", "updated_at", "video_url", "url"]
        read_only_fields = ["id", "created_at", "updated_at", "transcript"]

    def validate(self, attrs):
        if 'url' in attrs and 'video_url' not in attrs:
            attrs['video_url'] = attrs['url']
        return attrs

    def create(self, validated_data):
        if 'url' in validated_data:
            url = validated_data.pop('url')
            validated_data['video_url'] = url

            try:
                youtube_info = extract_youtube_info(url)
                validated_data['title'] = youtube_info.get('title', '')
                validated_data['description'] = youtube_info.get('description', '')
            except Exception as e:
                validated_data['title'] = ''
                validated_data['description'] = ''

            try:
                transcript = transcribe_yt_video(url)
                validated_data['transcript'] = transcript
            except Exception as e:
                print(f"Transciption error: {str(e)}")
                validated_data['transcript'] = f"Transciption failed: {str(e)}"

        return super().create(validated_data)