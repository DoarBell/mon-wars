from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
# Create your views here.

def index(request):
    return render(request, "monster/layout.html")

def login_view(request):
    # need to make this
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POsT["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #index doesnt exist yet
            return HttpResponse(reverse("index"))
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
    return HttpResponse(reverse("index"))

def register(request):
    #forgot you needed to register yourself
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POSt["confirmation"]
        if password != confirmation:
            return render(request, "monster/register.html",{
                "message": "Passwords doesn't match"
            })
        try:
            user=User.objects.create_user(username, username, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "monster/register.html",{
                "message": "Username already taken"
            })
        login(request, user)
        return HttpResponse(reverse("index"))
    else:
        return render(request, "monster/register.html")