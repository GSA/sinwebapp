from django.contrib import admin
from django.urls import path, include 
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings
from uaa_client.decorators import staff_login_required

admin.site.login = staff_login_required(admin.site.login)

urlpatterns = [
    path('admin/', admin.site.urls),
    # App Urls
    path('', include('authentication.urls', namespace='authentication')),
    path('api/', include('api.urls', namespace='api')),
    path('auth/', include('uaa_client.urls', namespace='uaa_client'))
]