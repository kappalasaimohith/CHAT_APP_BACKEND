from rest_framework.serializers import Serializer,ModelSerializer
from rest_framework  import serializers
from .models import *

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        return Room.objects.create(**validated_data)
    
class MessagesSerializer(ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model=Messages
        fields = '__all__'

    def get_username(self,obj):
        return obj.sent_by.username
    
    def create(self, validated_data):
        return Messages.objects.create(**validated_data)

class RoomMembersSerializer(ModelSerializer):
    class Meta:
        model = RoomMember
        fields  = '__all__'

    def create(self, validated_data):
        return RoomMember.objects.create(**validated_data)
    

class RoomRequestSerializer(ModelSerializer):
    room_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    class Meta:
        model = RoomRequests
        fields = '__all__'

    def get_username(self,obj):
        return obj.user.username

    def get_room_name(self,obj):
        return obj.room.room

    def create(self, validated_data):
        return RoomRequests.objects.create(**validated_data)