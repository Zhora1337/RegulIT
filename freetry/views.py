from django.shortcuts import render, redirect
from .forms import PhotoForm, ShowForm
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from .models import Photo
from django.shortcuts import get_object_or_404
from django.http import JsonResponse    
import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PhotoSerializer
from rest_framework import status

class ApiPhoto(APIView):

    def get(self, request, format = None):
        photo = Photo.objects.all()
        serialicer = PhotoSerializer(photo, many = True)
        return Response(data=serialicer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format = None):
        serializer = PhotoSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

def index(request):
    if request.method =='POST':
        form = PhotoForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            form.photo = form.cleaned_data['photo']
            photo = form.save(commit=False)
            print(photo.photo)
            #photo.user = request.user
            photo.save()
            photo_path = photo.photo.path
            print(photo_path)
            photo.height = photo.img_stat()[0]
            photo.width = json.dumps(photo.img_signs())
            form.save()
            os.remove(photo.photo.path)
            return JsonResponse({'error': False, 'photo': photo.photo.url, 'width': photo.width})
        else:
            return JsonResponse({'error': True, 'errors': form.errors})
    else:
        form = PhotoForm()
    return render(request, 'freetry/index.html',{'form':form})

def result(request, id):
    photo = get_object_or_404(Photo, id=id)
    return render(request, 'freetry/result.html',{'form':photo})


def show(request):
    users_photos = Photo.objects.all()
    for photo in users_photos:
        if photo.photo == '':
            photo.photo = 'none.png'
    return render(request, 'freetry/results.html',{'photos':users_photos})

