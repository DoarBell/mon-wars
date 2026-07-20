from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from .models import Monster

@receiver(m2m_changed, sender=Monster.special.through)
def limit_attacks(sender, instance, action, **kwargs):
    if action == "pre_add":
        if instance.special.count() + len(kwargs.get("pk_set", [])) > 3:
            raise ValidationError("Maximum 3 attacks allowed.")