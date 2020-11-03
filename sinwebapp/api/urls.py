from django.urls import path, include
from api import views_private
from api.serializers import SinViewSet, SinParamViewSet, StatusViewSet
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'sins', SinViewSet)
router.register(r'status', StatusViewSet)
router.register(r'search', SinParamViewSet, basename='SIN')

urlpatterns= [
    # application endpoints
    path('user/', views_private.user_info),
    path('users/', views_private.user_info_filtered),
    path('sinUser/', views_private.sin_user_info),
    path('sin/', views_private.sin_info),
    path('sins/', views_private.sin_info_all),
    path('updateSin/', views_private.sin_info_update),
    path('status/', views_private.status_info),
    path('userStatuses/', views_private.user_status_info),
    path('statuses/', views_private.status_info_all),
    # public endpoints
    path('v1/', include(router.urls))
]