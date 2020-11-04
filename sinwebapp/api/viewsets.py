from rest_framework import viewsets, generics
from rest_framework.response import Response

from django.contrib.auth.models import User

from api.serializers import SinSerializer, StatusSerializer
from api.models import Sin, Status

class SinViewSet(generics.ListAPIView):
    queryset = Sin.objects.all()
    serializer_class = SinSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        index = 1
        data = {}
        for i in serializer.data:
            data[index] = i
            index += 1

        metadata = { 'count': len(data) }
        results = { 'metadata': metadata, 'results': data }
        return Response(results)

class SinParamViewSet(generics.ListAPIView):
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

        if status is not None:
            search_status = Status.objects.get(name=status)
            queryset = queryset.filter(status=status)
    
        if sin_number is not None:
            queryset = queryset.filter(sin_number=sin_number)
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        index = 1
        data = {}
        for i in serializer.data:
            data[index] = i
            index += 1

        metadata = { 'count': len(data) }
        results = { 'metadata': metadata, 'results': data }
        return Response(results)

class StatusViewSet(generics.ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        index = 1
        data = {}
        for i in serializer.data:
            data[index] = i
            index += 1

        metadata = { 'count': len(data) }
        results = { 'metadata': metadata, 'results': data }
        return Response(results)