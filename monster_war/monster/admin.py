from django.contrib import admin
from .models import User, Trainer, Monster, Attacks, Effects

# Register your models here.
admin.site.register(User),
admin.site.register(Trainer),
admin.site.register(Monster),
admin.site.register(Attacks),
admin.site.register(Effects),
