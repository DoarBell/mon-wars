from django.contrib.auth.models import AbstractUser
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.dispatch import receiver
from django.db import models

class Trainer(models.Model):
    trainer_name = models.CharField(max_length=30)
    wins = models.IntegerField(default=0)
    looses = models.IntegerField(default=0)
    battles = models.IntegerField(default=0)
    luck = models.IntegerField(default=0)
    likessounds = models.BooleanField(default=False)

    def monster_count(self):
        return self.info.slaverist.count() if self.info else 0
    
    @property
    def win_ratio(self):
        if self.battles == 0:
            return 0
        return int((self.wins / self.battles) * 100)
    
    def __str__(self):
        return f"{self.trainer_name}"
    
class User(AbstractUser):
    trainer_info = models.OneToOneField(
        Trainer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="info"
    )
    def __str__(self):
        return f"{self.username} trainer name: {self.trainer_info if self.trainer_info else 'None'}"

class Effects(models.Model):
    thing = models.CharField(max_length=20)
    def __str__(self):
        return self.thing

class Attacks(models.Model):
    name = models.CharField(max_length=100)
    atk = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999999999)]
    )
    ability = models.ManyToManyField(Effects, blank=True)
    def __str__(self):
        return f"{self.name}"

class Monster(models.Model):
    owner = models.ManyToManyField(User, related_name="slaverist")
    name = models.CharField(max_length=30)
    lpoints = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )
    description = models.CharField(max_length=1000, default="Monster description")
    mon_atk_anim = models.ImageField(
        upload_to='monster_imgs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['png'])],
    )
    mon_img = models.ImageField(
        upload_to='monster/static/monster/images',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['png'])],
    )
    strength = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    defense = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    special = models.ManyToManyField(Attacks, related_name="attack")

    alive = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

