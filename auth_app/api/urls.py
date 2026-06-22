from django.urls import path
from .views import RegistrationView, CookieTokenObtainPairView, CookieRefreshView
from . import views

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('token/', CookieTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token-refresh'),
]