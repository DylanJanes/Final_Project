from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    displayName = models.CharField(max_length=100, default="Display Name")
    highscores = models.JSONField(default=dict, blank=True)

    def Scores(self, key, value):    #checks if key/game is in highscores if found and new highscore then updates highscores 
        if key in self.highscores:              
            if value > self.highscores[key]:
                self.highscores[key] = value
                self.save(update_fields=["highscores"])
            else:
                return
        else:
            self.highscores[key] = value            #if not found then updates highscores with key/game and value/score
            self.save(update_fields=["highscores"])

    def RemoveScore(self, key):      #removes score/value at given key/game
        if key in self.highscores:
            del self.highscores[key]
            self.save(update_fields=["highscores"])

