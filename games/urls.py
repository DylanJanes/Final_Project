# games/urls.py
from django.urls import path
from .views import SnakeGameView, play_godot_game

urlpatterns = [
    path("snake/", SnakeGameView.as_view(), name="snake"),
    path("sakoban/", play_godot_game, name="sakoban"),
]