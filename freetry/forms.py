from django import forms
from .models import Photo


class PhotoForm(forms.ModelForm):
    photo = forms.ImageField()
    class Meta:
        model = Photo
        fields = (
            'photo',
        )
