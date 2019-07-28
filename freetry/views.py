from django.shortcuts import render, redirect
from .forms import PhotoForm, ShowForm
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from .models import Photo
from django.shortcuts import get_object_or_404
import os



def index(request):
    if request.method =='POST':
        form = PhotoForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            form.photo = form.cleaned_data['photo']
            photo = form.save(commit=False)
            print(photo.photo)
            photo.user = request.user
            photo.save()
            photo.height = photo.img_stat()[0]
            photo.width = photo.img_stat()[1]
            form.save()
            os.remove(photo.photo.path)
            return redirect('result', id=photo.id)
    else:
        form = PhotoForm()
    return render(request, 'freetry/index.html',{'form':form})

def result(request, id):
    photo = get_object_or_404(Photo, id=id)
    return render(request, 'freetry/result.html',{'form':photo})


def show(request):
    users_photos = Photo.objects.filter(user=request.user)
    return render(request, 'freetry/results.html',{'photos':users_photos})

