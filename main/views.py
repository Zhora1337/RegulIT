from django.shortcuts import render

def index(request):
    from django.utils import translation
    # user_language = 'ru'
    # translation.activate(user_language)
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]

    return render(request, 'main/home.html')

def AboutUs(request):
    return render(request, 'main/AboutUs.html')

def ourgoal(request):
    return render(request, 'main/ourgoal.html')

def ourteam(request):
    return render(request, 'main/ourteam.html')