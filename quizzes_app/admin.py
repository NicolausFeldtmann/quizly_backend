from django.contrib import admin
from .models import QuizzModel, QuestionsModel

admin.site.register(QuizzModel)
admin.site.register(QuestionsModel)
