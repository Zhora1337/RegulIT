from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit_email/$', views.email, name='email'),
    url(r'^edit_names/$', views.names, name='names')
]