from django.db import models


class Player(models.Model):
    id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.id

class Game(models.Model):
    author = models.ForeignKey(Player, related_name="author", on_delete=models.CASCADE)
    guest = models.ForeignKey(Player, related_name="guest", blank=True, null=True, on_delete=models.CASCADE)
    number = models.IntegerField()
    is_finished = models.BooleanField(default=False)
    steps_before_win = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id} ({self.author.id} vs {self.guest.id if self.guest else None})'


# class PlayerGameInfo(models.Model):
#     player = models.ForeignKey(Player, on_delete=models.CASCADE)
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     steps_before_win = models.IntegerField()

