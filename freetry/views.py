from django.shortcuts import render, redirect
from .forms import PhotoForm
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from .models import Photo
from django.shortcuts import get_object_or_404
from django.http import JsonResponse    
import os
import json
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from .serializer import PhotoSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


@api_view(['GET'])
def photo_list(request):
    if request.method == 'GET':
        photo = Photo.objects.filter(id=int(dict(request.data)['id'][0]))
        print(type(photo))
        serializer = PhotoSerializer(photo, many=True)
        return Response(serializer.data)



def index(request):
    if request.method =='POST':
        form = PhotoForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            form.photo = form.cleaned_data['photo']
            photo = form.save(commit=False)
            #photo.user = request.user
            photo.save()
            photo_path = photo.photo.path
            #print(photo_path)
            photo.width = json.dumps(photo.img_signs())
            form.save()
            os.remove(photo.photo.path)
            return JsonResponse({'error': False, 'photo': photo.photo.url, 'width': photo.width})
        else:
            return JsonResponse({'error': True, 'errors': form.errors})
    else:
        form = PhotoForm()
    return render(request, 'freetry/index.html',{'form':form})



class FileUploadView(APIView):
    parser_class = (FileUploadParser,)
    def post(self, request, *args, **kwargs):
        file_serializer = PhotoSerializer(data=request.data)
        if file_serializer.is_valid():	
            photo = file_serializer.save()
            photo.width = photo.img_signs()
            photo.save()
            print(photo.photo.path)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
