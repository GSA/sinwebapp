from django.urls import path

from files import views

app_name = 'files'

urlpatterns = [
    path('upload/', views.upload_file),
    path('download/', views.download_file)
]