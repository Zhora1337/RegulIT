from django.conf.urls import url, include
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'api/photo/$', views.ApiPhoto.as_view(), name='photo_api'),
]