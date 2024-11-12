from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'homepage/index.html', {})

def home(request):
    return render(request, 'homepage/home.html', {})

def profile(request):
    return render(request, 'homepage/profile.html', {})