from django.db import models


class Human(models.Model):
    mail = models.EmailField()
    password = models.CharField(max_length=40)
