from django.urls import path
from .views import QuizzListCreateView, SingleQuizzView
from . import views

urlpatterns = [
    path('quizzes/', QuizzListCreateView.as_view(), name='quizz-list-create'),
    path('quizzes/<int:pk>/', SingleQuizzView.as_view(), name='quiz-detail'),
]