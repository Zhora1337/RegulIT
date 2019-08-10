from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from skimage import io
import json
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, os.path.join(BASE_DIR, 'static/python'))
import delete


class Photo(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    width = models.CharField(max_length=1000, name='width', blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, name='photo')
    
    def img_signs(self):
        if self.photo.path == None:
            print('none') 
        else:
            image_path = self.photo.path
            image1 = Image.open(self.photo.path, mode='r')
            image = io.imread(self.photo.path)
            signs = []
            for i in range(0, 66):
                signs.append(0)
            signs = delete.script(image1, image, image_path)
            
        print('called')
        return signs
                