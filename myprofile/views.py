from django.shortcuts import render
from . import forms
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect

def index(request):
    return render(request, 'myprofile/index.html',)


def email(request):
    return render(request, 'myprofile/edit_email.html')


def names(request):
    return render(request, 'myprofile/edit_names.html')
