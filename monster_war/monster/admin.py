from django.contrib import admin
from .models import Trainer, Monster, Attacks, Effects

# Register your models here.
admin.site.register(Trainer),
admin.site.register(Monster),
admin.site.register(Attacks),
admin.site.register(Effects),
