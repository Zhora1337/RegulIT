from django import forms
from django.contrib.auth.models import User


class UserProfile(forms.Form):
    first_name = User.first_name
    last_name = User.last_name
    email = User.email
    get_user_info = forms.CharField(max_length=20)