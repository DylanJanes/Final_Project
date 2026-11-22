from django.urls import path
from . import views

urlpatterns = [
    path("leaderboards/", views.highscore_view, name="leaderboards")
]
