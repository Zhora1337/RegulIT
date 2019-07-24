from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Photo(models.Model):
    height = models.IntegerField(default=0, name='height')
    width = models.IntegerField(default=0, name='width')
    photo = models.ImageField(blank=True, null=True, name='photo')
    

    def img_stat(self):
        if self.photo.path == None:
            print('none') 
        else:
            im = Image.open(self.photo.path, mode='r')
            print(im.size)
        print('called')
        return im.size
        