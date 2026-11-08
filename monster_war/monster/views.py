from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Trainer, Monster, User

# Create your views here.
def index(request):
    try:
        user = request.user
        trainer = user.trainer_info
        trainer_win = trainer.win_ratio
    except AttributeError:
        return render(request, "monster/index.html")
    else:
        return render(request, "monster/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #index doesnt exist yet
            return HttpResponseRedirect(reverse("index"))
        else:
            #login also doesnt exist yet
            return render(request, "monster/login.html" ,{
                "message": "Invalid email and/or password."
            })
    elif request.method == "GET":
        return render(request, "monster/login.html")
    
def logout_view(request):
    # and this
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    #forgot you needed to register yourself
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "monster/register.html",{
                "message": "Passwords doesn't match"
            })
        try:
            with transaction.atomic():
                trainer=Trainer.objects.create(trainer_name=username)
                user=User.objects.create_user(
                    username, email, password, trainer_info = trainer
                    )
        except IntegrityError as e:
            print(e)
            return render(request, "monster/register.html",{
                "message": "Username already taken"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "monster/register.html",{
            "message": "Something went wrong request must be POST method"
        })
    


def monster(request):
    monsters = Monster.objects.all()
    return render(request, "monster/monster.html",{
        "monsters": monsters
    })

def newMonster(request):
    return render(request, "monster/newMonster.html")

def monster_view(request, id):
    return render(request, "monster/specific.html")

def manual(request):
    return render(request, "monster/manual.html")

def training(request):
    return render(request, "monster/training.html")

def fight(request):
    return render(request, "monster/fight.html")