from django.db import models
from django.contrib.auth.models import User

class QuizzModel(models.Model):
    title = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField(max_length=200)
    
    def __str__(self):
        return self.title

class QuestionsModel(models.Model):
    quizz = models.ForeignKey(QuizzModel, on_delete=models.CASCADE, related_name='questions')
    question_title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)