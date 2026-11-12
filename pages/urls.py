from django.urls import path

from .views import HomePageView, LeaderBoardsView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("leaderboards/", LeaderBoardsView, name="leaderboards")
]
