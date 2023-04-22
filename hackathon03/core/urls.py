from django.contrib import admin
from django.urls import path, include

from core.models import Camera
from core.views import UserRegistrationView, UserLoginView, CameraView

urlpatterns = [
    path('api/v1/locate/number/<str:card_number>/', CameraView.as_view()),
    path('api/v1/register', UserRegistrationView.as_view()),
    path('api/v1/login', UserLoginView.as_view())
]
