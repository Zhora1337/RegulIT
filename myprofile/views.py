from django.contrib.auth.models import User
from .models import UserPhoto
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from .forms import EditProfileForm, RegistrationForm, EditUserPhoto


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


def edit(request, username):
    if request.method == 'POST':
        form1 = EditProfileForm(request.POST, instance=request.user)
        form2 = EditUserPhoto(request.POST, request.FILES, instance=request.user.userphoto)
        if form1.is_valid() and form2.is_valid():
            request.user.userphoto.user_photo = form2.cleaned_data['user_photo']
            form1.save()
            form2.save()
            return HttpResponseRedirect('/myprofile')
    else:
        form1 = EditProfileForm(instance=request.user)
        form2 = EditUserPhoto(instance=request.user.userphoto)

    return render(request, 'myprofile/edit.html', {
        'form1':form1,
        'form2':form2
    })
