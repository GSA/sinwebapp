from django.urls import path, include
from api import views_private
from api import views_public
from rest_framework import routers, serializers, viewsets
from api.models import Sin, Status

class SinSerializer(serializer.HyperlinkedModelSerializer):
    class Meta:
        model = Sin 
        fields = ['sin_number', 'sin_title', 'sin_description', 'begin_date', 'end_date']

class SinViewSet(viewsets.ModelViewSet):
    queryset = Sin.objects.all()
    serializer_class = SinSerializer

class StatusSerializer(serializer.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ['name','description']

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serialzer_class = StatusSerializer


router = routers.DefaultRouter()
router.register(r'sins', SinViewSet)
router.register(r'statuses', StatusViewSet)

app_name = 'api'

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
    path('v1/search', views_public.search),
    path('v1/sins', views_public.sins),
    path('v1/status', views_public.status),
    # rest framework
    path('v2/', include(router.urls))
]