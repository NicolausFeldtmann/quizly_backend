from rest_framework import serializers
from django.contrib.auth.models import User
from quizzes_app.models import QuizzModel, QuestionsModel
from quizzes_app.utils import extract_youtube_info, transcribe_yt_video, generate_quiz, normalize_yt_url
from django.core.exceptions import ValidationError

class QuestionsSerializer(serializers.ModelSerializer):
    """Serializer class to handle data for quiz containig questions."""

    class Meta:
        model = QuestionsModel
        fields = ["id", "question_title", "question_options", "answer", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

class QuizzSerializer(serializers.ModelSerializer):
    """Serializer class to handle and validate requests dedicated to quizes."""
    url = serializers.URLField(write_only=True, required=False)
    video_url = serializers.URLField(required=False)
    questions = QuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = QuizzModel
        fields = ["id", "title", "description", "created_at", "updated_at", "video_url", "url", "questions"]
        read_only_fields = ["id", "created_at", "updated_at", "questions"]

    def validate(self, attrs):
        """Checks if incommig request contains 'url'."""
        """Normalizes YouTube url format."""
        """Modifies 'url' to needed 'video_url' and returns modifed data."""
        if 'url' in attrs:
            try:
                normalized_url = normalize_yt_url(attrs['url'])
                attrs['video_url'] = normalized_url

                youtube_info = extract_youtube_info(normalized_url)
                attrs['_youtube_info'] = youtube_info
            except ValidationError as e:
                raise serializers.ValidationError(f"URL validation failed: {str(e)}")
            except Exception as e:
                raise serializers.ValidationError(f"Invalid YouTube URL: {str(e)}")
            attrs.pop('url')
        return attrs

    def create(self, validated_data):
        """Creates quiz. Saves 'title' and 'description'."""
        """Gets, transcribes and creates quiz out of audio from url."""

        url = validated_data.get('video_url')
        validated_data['video_url'] = url
        youtube_info = extract_youtube_info(url)
        validated_data['title'] = youtube_info.get('title', '')
        validated_data['description'] = youtube_info.get('description', '')
        transcript = transcribe_yt_video(url)
        validated_data['transcript'] = transcript

        quiz = super().create(validated_data)

        if quiz.transcript and not quiz.transcript.startswith("Transcription failed"):
            quiz_data = generate_quiz(quiz.transcript)

            if quiz_data.get("title"):
                quiz.title = quiz_data['title']

            if quiz_data.get("description"):
                quiz.description = quiz_data['description']
            quiz.save()

            questions_created = 0
            for question_data in quiz_data.get('questions', []):
                QuestionsModel.objects.create(
                    quizz=quiz,
                    question_title=question_data.get('question_title', ''),
                    question_options=question_data.get('question_options', []),
                    answer=question_data.get('answer', '')
                )
                questions_created += 1
        quiz.refresh_from_db()
        return quiz


class SingleQuizzSerializer(serializers.ModelSerializer):
    """Serializer class to handle single quiz rquests."""
    questions = QuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = QuizzModel
        fields = ["id", "title", "description", "transcript", "created_at", "updated_at", "video_url", "questions"]
        read_onlyFields = ["id", "created_at", "updated_at", "transcript", "questions"]

class UpdateSerializer(serializers.ModelSerializer):
    """Serializer class to handle PATCH requests of single quiz"""

    class Meta:
        model = QuizzModel
        fields = ["id", "title", "description"]
        read_only_fields = ["id"]