from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('success/', views.login_success, name='success')
]