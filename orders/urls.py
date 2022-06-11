from django.urls import path,include

from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("signin", views.signin, name="signin"),
]
