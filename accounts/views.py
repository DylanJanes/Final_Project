from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@require_POST
def submit_score(request):
    # Make sure the player is logged in
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not logged in"}, status=401)

    try:
        data = json.loads(request.body)

        game = data.get("game")
        score = data.get("score")

        if not isinstance(game, str) or not game:
            return JsonResponse({"error": "Invalid game"}, status=400)

        if type(score) is not int or score < 0:
            return JsonResponse({"error": "Invalid score"}, status=400)

        # Update the user's high score
        request.user.Scores(game, score)

        return JsonResponse({
            "success": True,
            "highscores": request.user.highscores
        })

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid request"}, status=400)