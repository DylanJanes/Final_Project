# games/urls.py
from django.urls import path
from .views import SnakeGameView

urlpatterns = [
    path("snake/", SnakeGameView.as_view(), name="snake"),
]