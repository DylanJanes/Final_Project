from django.urls import path
from . import views

from .views import HomePageView, play_godot_game

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("play/", views.play_godot_game, name="play_godot_game"),
    path("leaderboards/", LeaderBoardsView, name="leaderboards")
]
