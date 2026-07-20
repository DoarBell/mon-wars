from .models import Trainer, Monster

def monster_team(request):
    if request.user.is_authenticated:
        return {
            "monster_team": Monster.objects.filter(owner=request.user, alive=True,).select_related("owner").prefetch_related("special")
        }
    return {"monster_team": Monster.objects.none()}