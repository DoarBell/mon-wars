from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from PIL import Image
from .models import Trainer, Monster, User, Attacks
import random
# In case you forget about it your username is kijuro and the pasword is 123
# honestly if you forget about it I'll be very disapointed

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
    monsters = Monster.objects.filter(owner=request.user.id)
    return render(request, "monster/monster.html",{
        "monsters": monsters
    })

def newatk(request):
    new_atk = Attacks.objects.order_by('?').first()
    if new_atk is None:
        return JsonResponse({"error": "No attacks found"}, status=404)
    request.session["rolled_attack"]= new_atk.name
    return JsonResponse({"attack": new_atk.name, "atk": new_atk.atk })

def pixelate(path, pixel_size=6):
    img =Image.open(path)
    small = img.resize(
        (max(1, img.width // pixel_size), max(1, img.height // pixel_size)),
        resample=Image.BILINEAR,
    )
    small.resize(img.size, Image.NEAREST).save(path)

@login_required
def newMonster(request):
    if request.method == "GET":
        return render(request, "monster/newMonster.html")
    try:
        name = request.POST["name"].strip()
        if not name:
            return render(request, "monster/newMonster.html", {
                "message": "Error, monster must have a name"
            })
        description = request.POST["description"]
        img = request.FILES["image"]
        max_lpoints = random.randint(200, 1000)
        strength = random.randint(1, 100)
        defense = random.randint(1, 100)
        attack_name = request.session.pop("rolled_attack", None)
        special = Attacks.objects.filter(name=attack_name).first()
        if special is None:
            return render(request, "monster/newMonster.html", {
                "message": "Error, roll an attack"
            })
    except MultiValueDictKeyError:
        return render(request, "monster/newMonster.html", {
            "message" : "Error when creating new monster"
        })
    else:
        new_mon = Monster(
            name = name,
            strength = strength,
            defense = defense,
            mon_img = img,
            description = description,
            max_lpoints = max_lpoints,
            lpoints = max_lpoints,
        )
        new_mon.save()
        try:
            pixelate(new_mon.mon_img.path)
        except Exception:
            new_mon.mon_img.delete(save=False)
            new_mon.delete()
            return render(request, "monster/newMonster.html", {
                "message": "Error, invalid image"
            })
        new_mon.owner.add(request.user)
        new_mon.special.add(special)
        return redirect("/monster")


def monster_view(request, id):
    return render(request, "monster/specific.html")

def manual(request):
    return render(request, "monster/manual.html")

def training(request):
    return render(request, "monster/training.html")

def fight(request):
    return render(request, "monster/fight.html")