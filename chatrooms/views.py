from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
# Create your views here.
class CreateRoomView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self,request):
        room_name = request.data['room_name']
        userpk = CustomUser.objects.get(username= request.user).pk
        data={
            "room_name":room_name,
            "created_by":userpk,
        }
        serializer = RoomSerializer(data = data)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"message":"New room created"},status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        room_details = Room.objects.all()
        serializer = RoomSerializer(room_details,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)