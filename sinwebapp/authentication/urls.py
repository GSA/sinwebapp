from django.urls import path
from django.contrib.auth import views as auth_views
from core import settings 
from . import views

app_name = 'authentication'

if settings.APP_ENV != 'mcaas':
    urlpatterns = [
        path('', views.login_page, name='login'),
        path('logout/', views.logout_page, name='logout-splash'),
        path('success/', views.login_success_page, name='success')
    ]
else:
    urlpatterns = [
        path('', views.login_page, name='login'),
        path('auth/login/', auth_views.LoginView.as_view(template_name='login_form.html'), name='login-form'),
        path('logout/', views.logout_page, name='logout-splash'),
        path('success/', views.login_success_page, name='success')
    ]