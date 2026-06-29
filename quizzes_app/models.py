from django.db import models
from django.contrib.auth.models import User

class QuizzModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes', default="")
    title = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(blank=True, default="")
    transcript = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField(max_length=200)
    
    def __str__(self):
        return self.title

class QuestionsModel(models.Model):
    quizz = models.ForeignKey(QuizzModel, on_delete=models.CASCADE, related_name='questions')
    question_title = models.CharField(max_length=30, default="")
    question_options = models.JSONField(max_length=500, default=list)
    answer = models.CharField(max_length=500, default="")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_title