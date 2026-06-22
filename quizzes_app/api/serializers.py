from rest_framework import serializers
from django.contrib.auth.models import User
from quizzes_app.models import QuizzModel, QuestionsModel
from quizzes_app.utils import exract_youtube_info

class QuizzSeriazlizer(serializers.ModelSerializer):
    url = serializers.URLField(write_only=True, required=False)

    class Meta:
        model = QuizzModel
        fields = ["id", "title", "description", "created_at", "updated_at", "video_url", "url"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        if 'url' in validated_data:
            url = validated_data.pop('url')
            validated_data['video_url'] = url

            try:
                youtube_info = exract_youtube_info(url)
                validated_data['title'] = youtube_info.get('title', '')
                validated_data['description'] = youtube_info.get('description', '')
            except Exception as e:
                validated_data['title'] = ''
                validated_data['description'] = ''

        return super().create(validated_data)