from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def register(request):
    return render(request, 'orders/register.html')

def signin(request):
    return render(request, 'orders/signin.html')