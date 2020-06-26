from django.urls import path

from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout, name='logout'),
    path('success/', views.login_success, name='success')
]