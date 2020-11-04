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