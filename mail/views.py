from django.shortcuts import render
from django.core.mail import send_mail

def index(request):

    send_mail('ваш промокод', '35285dh', 'aregulov@yandex.ru',[request.user.email], fail_silently=False)

    return render(request, 'mail/index.html')