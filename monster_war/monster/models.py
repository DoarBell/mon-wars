from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.db import models

#Make your migrations here
class Trainer(models.Model):
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
    
class Effects(models.Model):
    thing = models.CharField(max_length=20)

class Attacks(models.Model):
    name = models.CharField(max_length=100)
    atk = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999999999)]
    )
    ability = models.ForeignKey(Effects, on_delete=models.CASCADE)

class Monster(models.Model):
    name = models.CharField(max_length=30)
    mon_img = models.ImageField(
        upload_to='gifs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['gif'])],
    )
    str = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    defense = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    special = models.ForeignKey(Attacks, on_delete=models.CASCADE)

    