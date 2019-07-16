from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.MainView.as_view()),
    url(r'^AboutUs/', views.AboutUs, name= 'AboutUs'),
    url(r'^ourgoal/', views.ourgoal, name= 'ourgoal'),
    url(r'^ourteam/', views.ourteam, name= 'ourteam'), 
    #url(r'^logout/', views.LogoutView.as_view()),
]