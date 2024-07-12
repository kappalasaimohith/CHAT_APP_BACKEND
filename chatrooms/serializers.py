from rest_framework.serializers import Serializer,ModelSerializer
from rest_framework  import serializers
from .models import *

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        return Room.objects.create(**validated_data)