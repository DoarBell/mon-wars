from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

#Make your migrations here
class User(models.Model):
    trainer_name = models.OneToOneField(User, on_delete=models.CASCADE)
    wins = models.IntegerField()
    looses = models.IntegerField()
    battles = models.IntegerField()
    luck = models.IntegerField()
    def monster_count(self):
        return self.monster.count()
    
    @property
    def win_ratio(self):
        if self.battles == 0:
            return 0
        return int((self.wins/self.battles) * 100)
    
    def __str__(self):
        return f"{self.user.username} win ratio of {self.win_ratio}"
    
class effects(models.Model):
    thing = models.CharField(max_length=20)

class attacks(models.Model):
    name = models.CharField(max_length=100)
    atk = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999999999)]
    )
    ability = models.ForeignKey(effects, on_delete=models.CASCADE)

class monster(models.Model):
    name = models.CharField(max_length=30)
    str = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    defense = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    special = models.ForeignKey(attacks, on_delete=models.CASCADE)

    