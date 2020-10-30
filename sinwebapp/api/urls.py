from django.urls import path, include
from api import views_private
from api import views_public
from rest_framework import routers, serializers, viewsets
from api.models import Sin, Status

app_name = 'api'

# REST Framework Serializers and Viewsets 

class SinSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.StringRelatedField(many=False)
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = Sin 
        fields = ['sin_number', 'sin_title', 'sin_description', 'status', 'user']

class SinViewSet(viewsets.ModelViewSet):
    queryset = Sin.objects.all()
    serializer_class = SinSerializer

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ['name','description']

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

# URL Routing

router = routers.DefaultRouter()
router.register(r'sins', SinViewSet)
router.register(r'statuses', StatusViewSet)

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
    # rest framework endpoints
    path('v2/', include(router.urls))
]