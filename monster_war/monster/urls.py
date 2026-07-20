from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("monster", views.monster, name="monster"),
    path("manual", views.manual, name="manual"),
    path("training", views.training, name="training"),
    path("fight", views.fight, name="fight"),
]