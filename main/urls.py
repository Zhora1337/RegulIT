from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^AboutUs/', views.AboutUs, name= 'AboutUs'),
    url(r'^ourgoal/', views.ourgoal, name= 'ourgoal'),
    url(r'^ourteam/', views.ourteam, name= 'ourteam'), 
]