from django.shortcuts import render

def index(request):
    return render(request, 'main/home.html')

def AboutUs(request):
    return render(request, 'main/AboutUs.html')

def ourgoal(request):
    return render(request, 'main/ourgoal.html')

def ourteam(request):
    return render(request, 'main/ourteam.html')