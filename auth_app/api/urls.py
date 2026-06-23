from django.urls import path
from .views import RegistrationView, CookieTokenObtainPairView, CookieRefreshView
from . import views

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', CookieTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token-refresh'),
]