from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit_email/$', views.email, name='email'),
    path('edit/<str:username>/', views.edit),
]