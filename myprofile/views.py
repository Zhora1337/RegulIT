from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import UserForm


def index(request):
    return render(request, 'myprofile/index.html')


def email(request):
    return render(request, 'myprofile/edit_emal.html')

def edit(request, id):
    user = User.objects.get(id=id)
    user_form = UserForm(request.POST, instance=user)
    user_form.save()
    return render(request, 'myprofile/edit.html', {'user_form': user_form})

