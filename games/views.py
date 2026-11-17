from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class SnakeGameView(TemplateView):
    template_name = "games/snake.html"

def play_godot_game(request):
    return render(request, "games/sakoban.html")