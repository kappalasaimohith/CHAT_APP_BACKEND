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
        room = request.data['room']
        userpk = CustomUser.objects.get(username= request.user).pk
        data={
            "room":room,
            "created_by":userpk,
        }
        
        serializer = RoomSerializer(data = data)
        if (serializer.is_valid()):
            obj = serializer.save()
            print("room is ", obj)
            data2 = {
                "user": userpk,
                "room": Room.objects.get(room = obj).pk
            }
            MemberSerializer = RoomMembersSerializer(data = data2)
            if MemberSerializer.is_valid(): 
                obj2 = MemberSerializer.save()
                obj2_instance = RoomMember.objects.get(room = Room.objects.get(room = obj).pk )
                obj2_instance.owner = True
                obj2_instance.save()

                print(obj2, " is the object of ")
                return Response({"message":"New room created "},status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        room_details = Room.objects.filter(created_by = request.user)
        serializer = RoomSerializer(room_details,many=True)
        print(serializer.data, " is the room data")
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class GetMessages(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request,id):
        # room_name = Room.objects.get(room_id = id)
        messages = Messages.objects.filter(room_id=id)
        serializer = MessagesSerializer(messages)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


class RoomsToJoinView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        user = request.user
        userpk = user.pk
        allRooms = Room.objects.exclude(created_by=userpk)
        room_list = []
        new_room_list = []

        for room in allRooms:
            try:
                RoomMember.objects.get(room=room.pk, user=userpk)
            except RoomMember.DoesNotExist:
                room_list.append(room)
        for room in room_list:
            try:
                RoomRequests.objects.get(room = room.pk, user = userpk)
            except RoomRequests.DoesNotExist:
                new_room_list.append(room)
        serializer = RoomSerializer(new_room_list, many=True)

    
        print(serializer.data, " is the serializer data")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user= request.user
        userpk = user.pk
        data = {
            "room": request.data['room_id'],
            "user": userpk,
        }
        request_serializer = RoomRequestSerializer(data=data)
        if request_serializer.is_valid():
            request_serializer.save()
            return Response({"success": "Request sent successfully"}, status=status.HTTP_200_OK)
        else:
            print(request_serializer.errors)
            return Response({"error": "There is an error in the request"}, status=status.HTTP_400_BAD_REQUEST)

class GetMyRequests(APIView):
    def get(self, request):
        userpk = request.user.pk
        requested_data = RoomRequests.objects.filter(user =userpk)
        print(list(requested_data))
        request_serializer  = RoomRequestSerializer(requested_data, many=True)
        
        return Response(request_serializer.data, status=status.HTTP_200_OK)
    
class GetOtherRequests(APIView):
    def get(self, request):
        userpk = request.user.pk
        requested_data = RoomRequests.objects.exclude(user = userpk)
        request_serializer = RoomRequestSerializer(requested_data, many= True)
        return Response(request_serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        print(request.data, " is teh data")
        userpk = CustomUser.objects.get(id = request.data['user']).pk
        roompk = Room.objects.get(id = request.data['room_name']).pk
        data = {
            'room': roompk,
            'user': userpk,
            "member": True
        }
        RoomRequestInstance = RoomRequests.objects.get(room = roompk , user = userpk)
        RoomRequestInstance.status = request.data['status']
        RoomRequestInstance.save()
        room_member_serializer = RoomMembersSerializer(data= data)
        if(room_member_serializer.is_valid()):
            room_member_serializer.save()
            return Response({"success":"status updated"},status=status.HTTP_202_ACCEPTED)
        else:
            print(room_member_serializer.errors)
            return Response({"error":"There is an error"}, status=status.HTTP_400_BAD_REQUEST)
        
class GetAllEligibleRooms(APIView):
    def get(self, request):
        rooms = Room.objects.filter(created_by = request.user.pk)
        room_serializer = RoomSerializer(rooms, many = True)
        rooms2  = RoomMember.objects.filter(user = request.user.pk).filter(member = True)
        rooms2_serializer = RoomMembersSerializer(rooms2, many=True)
        return Response({"rooms": room_serializer.data, "rooms2":rooms2_serializer.data },status= status.HTTP_200_OK)
        
class ViewMessages(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, id):
        messages = Messages.objects.filter(room=id)
        message_serializer = MessagesSerializer(messages, many=True)
        print(message_serializer.data, " is teh serializer data to send")
        return Response(message_serializer.data, status=status.HTTP_200_OK)

    