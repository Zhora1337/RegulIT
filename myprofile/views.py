from django.shortcuts import render
from . import forms

from django.http import HttpResponseRedirect

def index(request):
    if request.method == 'POST':
        form = forms.UserProfile(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = forms.UserProfile
    return render(request, 'myprofile/index.html', {'form': form})

