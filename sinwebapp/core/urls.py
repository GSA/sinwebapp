from django.contrib import admin
from django.urls import path, include 
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # App Urls
    path('', include('authentication.urls', namespace='authentication')),
    path('api/', include('api.urls', namespace='api')),
    path('auth/', include('uaa_client.urls', namespace='uaa_client'))
]