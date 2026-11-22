from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from accounts.models import CustomUser

@login_required
def highscore_view(request):
    if request.method == "POST":
        game_key = request.POST.get("game_key")
        score = int(request.POST.get("score", 0))    #saves games scores 

        request.user.Scores(game_key, score)     #sends to accounts.models.Scores to check the key with the value and update if needed. 

        return redirect("leaderboards")

    accounts = CustomUser.objects.all()
    return render(request, "leaderboards/leaderboards.html", {"accounts": accounts})