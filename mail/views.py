from django.shortcuts import render
from django.core.mail import send_mail
from mail.models import random_promocode

def index(request):
    code = random_promocode()
    send_mail('ваш промокод', code, 'admin@face2face.world',[request.user.email], fail_silently=False)
    return render(request, 'mail/index.html')