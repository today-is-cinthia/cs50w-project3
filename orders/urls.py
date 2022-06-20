from django.urls import path,include
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("signin", views.signin, name="signin"),
    path("home", views.home, name="home"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("menu", views.menu, name="menu"),
    path("obtener_precio", views.obtener_precio, name="obtener_precio"),
    path("cart", views.cart, name="cart"),
]
