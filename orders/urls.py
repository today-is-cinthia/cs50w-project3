from django.urls import path,include
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("signin", views.signin, name="signin"),
    path("home", views.home, name="home"),
]
