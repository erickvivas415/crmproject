from django.shortcuts import render
from .models import User, Members, Profile, Profession

# Create your views here.

def index(request):
    return render(request, 'homepage/index.html', {})

def home(request):
    return render(request, 'homepage/home.html', {})

def profile(request):
    return render(request, 'homepage/profile.html', {})


def resumeboard(request):
    userdb = User.objects.all()
    return render(request, 'resumeboard.html', {'userdb': userdb})