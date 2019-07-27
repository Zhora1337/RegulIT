from django.shortcuts import render
from .forms import PhotoForm, ShowForm
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from .models import Photo
from django.shortcuts import get_object_or_404



def index(request):
    if request.method =='POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.photo = form.cleaned_data['photo'] 
            form.save()
            photo = Photo.objects.latest('id')
            photo.height = photo.img_stat()[0]
            photo.width = photo.img_stat()[1]
            photo.save()
            return HttpResponseRedirect('/freetry/results/')
    else:
        form = PhotoForm()
    return render(request, 'freetry/index.html',{'form':form})

def result(request, id):
    photo = get_object_or_404(Photo, id=id)
    photo.height = photo.img_stat()[0]
    photo.width = photo.img_stat()[1]
    stat = ShowForm(instance=photo)
    return render(request, 'freetry/result.html',{'form':stat})


def show(request):
    photos = Photo.objects.all()
    return render(request, 'freetry/results.html',{'photos':photos})

