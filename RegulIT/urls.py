"""RegulIT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('main.urls')),
    url(r'^findlove/', include('findlove.urls')),
    url(r'^friend/', include('friend.urls')),
    url(r'^person/', include('person.urls')),
    url(r'^for_companies/', include('for_companies.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^helper/', include('helper.urls')),
    url(r'^guidance/', include('guidance.urls')),
    url(r'^compatibility/', include('compatibility.urls')),   
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^freetry/', include('freetry.urls')),
    url(r'^myprofile/', include('myprofile.urls')),
    url(r'^result/', include('result.urls')),
]
from django.conf import settings
from django.conf.urls.static import static
# ... your normal urlpatterns here

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns =i18n_patterns(
#   url(r'^', include('main.urls')),
#    url(r'^signup/', include('signup.urls')),
#    url(r'^signin/', include('signin.urls')),
#    url(r'^findlove/', include('findlove.urls')),
#    url(r'^friend/', include('friend.urls')),
#    url(r'^person/', include('person.urls')),
#    url(r'^for_companies/', include('for_companies.urls')),
#)
