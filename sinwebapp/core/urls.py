from django.contrib import admin
from django.urls import path, include 
from django.conf.urls import url
from uaa_client.decorators import staff_login_required
from . import settings

admin.site.login = staff_login_required(admin.site.login)

urlpatterns = [
    path('admin/', admin.site.urls),
    # App Urls
    path('', include('authentication.urls', namespace='authentication')),
    path('api/', include('api.urls', namespace='api')),
    path('files/', include('files.urls', namespace='files')),
    path('auth/', include('uaa_client.urls', namespace='uaa_client'))
]