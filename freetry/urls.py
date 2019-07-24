from django.conf.urls import url, include
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'results/$', views.show),
    path('result/<int:id>', views.result, name='result')
]