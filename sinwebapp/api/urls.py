from django.urls import path
from . import views

app_name = 'api'

urlpatterns= [
    path('user/', views.get_user_info),
    path('sin/', views.get_sin_info),
    path('sins/', views.get_all_sins_info)
]