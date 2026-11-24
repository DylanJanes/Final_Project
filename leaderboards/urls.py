from django.urls import path
from . import views

urlpatterns = [
    path("", views.highscore_view, name="leaderboards")
]
