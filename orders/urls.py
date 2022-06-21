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
    path("checkout", views.checkout, name="checkout"),
    path("mark_complete/<int:order_item_id>", views.mark_complete, name="mark_complete"),
    path("remove/<int:cart_item_id>/", views.remove, name='remove'),
]
