from django.urls import path
from .views import QuizzListCreateView
from . import views

urlpatterns = [
    path('quizzes/', QuizzListCreateView.as_view(), name='quizz-list-create'),
]