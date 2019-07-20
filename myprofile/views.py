from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.forms import UserChangeForm
from .forms import EditProfileForm, RegistrationForm


def index(request):
    args = {'user':request.user}
    return render(request, 'myprofile/index.html', args)


def email(request):
    return render(request, 'myprofile/edit_emal.html')


def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            form = RegistrationForm()

            args = {'form':form}
            return render(request, '/myprofile/', args)


def edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/myprofile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'myprofile/edit.html', {'form':form})

