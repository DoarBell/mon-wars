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
    name = models.CharField(max_length=20)

class Attacks(models.Model):
    name = models.CharField(max_length=100)
    atk = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999999999)]
    )
    acuracy = models.IntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(100)],
        default=100
    )
    def __str__(self):
        return f"{self.name}"

class Monster(models.Model):
    owner = models.ManyToManyField(User, related_name="slaverist")
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    max_lpoints = models.IntegerField(
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
    )
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
    strength = models.IntegerField()
    defense = models.IntegerField()
    speed = models.IntegerField(default=20)
    special = models.ManyToManyField(Attacks, related_name="attack")

    alive = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

class Stage(models.Model):
    order = models.PositiveIntegerField()
    enemy = models.ForeignKey(Monster, on_delete=models.PROTECT)
    is_boss = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]

class Card(models.Model):
    boost = models.CharField(max_length=20)
    amount = models.IntegerField()
    description = models.CharField(max_length=40)

class Run(models.Model):
    player = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    monster = models.ForeignKey(Monster, on_delete=models.PROTECT)
    current_stage = models.PositiveIntegerField(default=1)
    cards = models.ManyToManyField(Card, blank=True)
    status = models.CharField(max_length=10, default="active")

