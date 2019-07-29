from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from skimage import io
import json
import sys
sys.path.insert(1, 'C:/Users/GraySnow/Documents/GameMakerStudio2/lockstep-rollback/RegulIT/static/python')

import delete


class Photo(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.IntegerField(default=0, name='height')
    width = models.CharField(max_length=1000, name='width')
    photo = models.ImageField(blank=True, null=True, name='photo')
    

    def img_stat(self):
        if self.photo.path == None:
            print('none') 
        else:
            im = Image.open(self.photo.path, mode='r')
            print(im.size)
            print('called')
            return im.size
    
    def img_signs(self):
        if self.photo.path == None:
            print('none') 
        else:
            image1 = Image.open(self.photo.path, mode='r')
            image = io.imread(self.photo.path)
            signs = []
            for i in range(0, 66):
                signs.append(0)
            signs = delete.script(image1, image)
            
        print('called')
        return signs