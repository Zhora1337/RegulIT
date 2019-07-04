from django.shortcuts import render

def index(request):
    return render(request, 'for_companies/index.html')
