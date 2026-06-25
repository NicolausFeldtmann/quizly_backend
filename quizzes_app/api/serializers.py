from rest_framework import serializers
from django.contrib.auth.models import User
from quizzes_app.models import QuizzModel, QuestionsModel
from quizzes_app.utils import extract_youtube_info, transcribe_yt_video, generate_quiz

class QuestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionsModel
        fields = ["id", "question_title", "question_options", "answer", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

class QuizzSerializer(serializers.ModelSerializer):
    url = serializers.URLField(write_only=True, required=False)
    video_url = serializers.URLField(required=False)
    questions = QuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = QuizzModel
        fields = ["id", "title", "description", "transcript", "created_at", "updated_at", "video_url", "url", "questions"]
        read_only_fields = ["id", "created_at", "updated_at", "transcript", "questions"]

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
                print(f"YouTube info extraction error: {str(e)}")
                validated_data['title'] = ''
                validated_data['description'] = ''

            try:
                transcript = transcribe_yt_video(url)
                validated_data['transcript'] = transcript
            except Exception as e:
                print(f"Transcription error: {str(e)}")
                validated_data['transcript'] = f"Transcription failed: {str(e)}"

        quiz = super().create(validated_data)

        if quiz.transcript and not quiz.transcript.startswith("Transcriptio fialed"):
            try:
                print("Generating quiz from transcript...")
                quiz_data = generate_quiz(quiz.transcript)

                if quiz_data.get('title'):
                    quiz.title = quiz_data['title']

                if quiz_data.get('description'):
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

                print(f"Successfully created {questions_created} questions")

            except Exception as e:
                print(f"Quiz generation error: {str(e)}")
                import traceback
                traceback.print_exc()

        quiz.refresh_from_db()
        return quiz