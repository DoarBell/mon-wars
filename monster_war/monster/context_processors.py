from .models import Trainer, Monster, User

def monster_team(request):
    if request.user.is_authenticated:
        return {
            "monster_team": Monster.objects.filter(owner=request.user, alive=True,).prefetch_related("special")
        }
    return {"monster_team": Monster.objects.none()}

def trainer(request):
    if request.user.is_authenticated:
        return {
            "trainer_info": getattr(request.user, "trainer_info", None)
        }
    return {"trainer_info": None}