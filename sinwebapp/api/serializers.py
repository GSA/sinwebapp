from rest_framework import serializers, viewsets
from api.models import Sin, Status
from django.contrib.auth.models import User

class SinSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.StringRelatedField(many=False)
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = Sin 
        fields = ['sin_number', 'sin_title', 'sin_description', 'status', 'user']

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ['id','name','description']

class SinViewSet(viewsets.ModelViewSet):
    queryset = Sin.objects.all()
    serializer_class = SinSerializer

class SinParamViewSet(viewsets.ModelViewSet):
    serializer_class = SinSerializer

    def get_queryset(self): 
        queryset = Sin.objects.all()
        sin_number = self.request.query_params.get('sin_number', None)
        user_email = self.request.query_params.get('user_email', None)
        user_id = self.request.query_params.get('user_id', None)
        status_id = self.request.query_params.get('status_id', None)
        status = self.request.query_params.get('status',None)

        if user_id is not None:
            search_user = User.objects.get(id=user_id)
            queryset = queryset.filter(user=search_user)

        if user_email is not None:
            search_user = User.objects.get(email=user_email)
            queryset = queryset.filter(user=search_user)
        
        if status_id is not None:
            search_status = Status.objects.get(id=status_id)
            queryset = queryset.filter(status=search_status)
    
        if sin_number is not None:
            queryset = queryset.filter(sin_number=sin_number)
        
        if status is not None:
            queryset = queryset.filter(status=status)

        return queryset



class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer