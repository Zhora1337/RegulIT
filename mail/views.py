from django.shortcuts import render
from django.core.mail import send_mail

def index(request):

    send_mail('ваш промокод', '35285dh', 'ya.seva910@yandex.ru',['ya.seva91098@gmail.com'], fail_silently=False)

    return render(request, 'mail/index.html')