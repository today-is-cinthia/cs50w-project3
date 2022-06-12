from ast import Pass
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.
def register(request):
    if request.method == "POST":
        first_name = request.POST['name']
        last_name = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        confirm = request.POST['confirm']

        if not username or not email or not password or not confirm or not first_name or not last_name or password != confirm:
            messages.success(request, "There was an error with your registration")
            return redirect('register')

        try:
            User.objects.create_user(username, email, password)
        except:
            return messages.success(request, "There was an error with your registration")
            return redirect('register')

        User.first_name = first_name
        User.last_name = last_name
        return redirect('signin')

    return render(request, 'orders/register.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user  = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return messages.success(request, "There was an error with your Sign in")
            return redirect('signin')
    return render(request, 'orders/signin.html')   

def home(request):
    return render(request, 'orders/home.html')