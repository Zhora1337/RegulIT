from . import views
from django.conf.urls import url

urlpattern = [
    url(r'^$', views.index, name='result')
]

