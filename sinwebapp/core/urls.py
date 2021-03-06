from django.contrib import admin
from django.urls import path, include 
from django.conf.urls import url
from uaa_client.decorators import staff_login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    # App Urls
    path('', include('authentication.urls', namespace='authentication')),
    path('api/', include('api.urls', namespace='api')),
    path('files/', include('files.urls', namespace='files')),
]

if not(settings.APP_ENV  == 'mcaas' or settings.APP_ENV == 'local_mcaas'):
    admin.site.login = staff_login_required(admin.site.login)
    urlpatterns += [path('auth/', include('uaa_client.urls', namespace='uaa_client'))]