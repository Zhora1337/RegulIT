from django.shortcuts import render

def index(request):
    return render(request, 'main/home.html')

def AboutUs(request):
    return render(request, 'main/AboutUs.html')