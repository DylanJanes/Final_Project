from django.views.generic import TemplateView
from django.shortcuts import render

def play_godot_game(request):
    return render(request, "godot_game.html")

class HomePageView(TemplateView):
    template_name = "home.html"

def LeaderBoardsView(request):
    context = {
        "games_list": ["Game_1", "Game_2", "Game_3"],
    }
    return render(request, "leaderboards.html", context)

