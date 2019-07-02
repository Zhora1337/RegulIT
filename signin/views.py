from django.shortcuts import render

def index(request):
    return render(request, 'signin/signin.html')
