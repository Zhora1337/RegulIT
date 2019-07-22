from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserPhoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_photo = models.ImageField(default='/none.png')
