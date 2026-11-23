from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import HighScore
from django.urls import reverse

games = {
    "snake": {"name": "Snake", "higher_is_better": True},
    "sakoban": {"name": "Sakoban", "higher_is_better": False},
    #add fields when new game is added higher_is_better True is higher score better False lower score is better
}


@login_required
def highscore_view(request):
    if request.method == "POST":
        game_key = request.POST.get("game_key")
        game = games.get(game_key)
        score = int(request.POST.get("score", ""))    #saves games scores 

        HighScore.record_score(    #saves score or updates highscore
            request.user,
            game_key,
            score,
            higher_is_better=game["higher_is_better"],
        )
        return redirect("leaderboards")

    boards = []

    for game_key, game in games.items():
        game_scores = HighScore.objects.filter(game_key=game_key)    #creates the leaderboards
        sort_field = "-score" if game["higher_is_better"] else "score"

        boards.append({
            "game_key": game_key, #used for test button delete when games are up
            "game_name": game["name"],
            "entries": game_scores.select_related("user")       #gets top 10 scores and their users
                .order_by(sort_field, "id")[:10],        
            "high_score": game_scores.filter(user=request.user)  #gets users best score for the game
                .values_list("score", flat=True).first(),
        })
    return render(request, "leaderboards/leaderboards.html", {"boards" :boards,})