from django.shortcuts import render
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.views.generic.edit import FormView


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


class MainView(TemplateView):
    template_name = 'main/home.html'

    def get(self, request):
        return render(request, self.template_name, {})