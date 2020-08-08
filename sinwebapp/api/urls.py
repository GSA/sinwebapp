from django.urls import path
from . import views

app_name = 'api'

urlpatterns= [
    path('user/', views.user_info),
    path('users/', views.user_info_filtered),
    path('sinUser/', views.sin_user_info),
    path('sin/', views.sin_info),
    path('sins/', views.sin_info_all),
    path('updateSin/', views.sin_info_update),
    path('status/', views.status_info),
    path('statuses/', views.status_info_all)
]