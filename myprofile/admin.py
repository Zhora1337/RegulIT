from django.contrib import admin
from .models  import UserPhoto

class UserPhotoAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserPhoto, UserPhotoAdmin)