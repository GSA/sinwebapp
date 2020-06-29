from django.urls import path
from django.contrib.auth import logout

from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout-splash'),
    path('success/', views.login_success_page, name='success')
]