from django.conf.urls import url, include
from . import views
from django.urls import path
from rest_framework.authtoken import views as authviews

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('api-token-auth/', authviews.obtain_auth_token),
    path('api/photo/', views.FileUploadView.as_view()),
]