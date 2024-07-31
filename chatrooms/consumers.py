from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import Room, Messages, CustomUser
from rest_framework_simplejwt.exceptions import InvalidToken
from .serializers import MessagesSerializer

class AsyncChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if not user.is_authenticated:
            await self.close()
            return
        self.userpk = user.pk
        self.user = user.username
        self.room_id = self.scope['url_route']['kwargs']['id']
        self.room_name = await sync_to_async(self.get_room_name)(self.room_id)
        self.room_pk = await sync_to_async(self.get_room_pk)(self.room_id)

        room_messages = await sync_to_async(self.get_room_messages)(self.room_pk)
        self.serializer = await sync_to_async(self.serialize_messages)(room_messages)

        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

        # Send initial messages to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'initial_messages',
            'messages': self.serializer,
            "user": self.user,
            "room_name":self.room_name
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(text_data, " is the data received")
        data = json.loads(text_data)
        message_content = data.get('message')

        # Create message data
        message_data = {
            'room': self.room_pk,
            'message': message_content,
            'sent_by': self.userpk
        }
        
        new_message_serializer = await sync_to_async(self.serializer_create_message)(message_data)
        if new_message_serializer:
            message = new_message_serializer.data
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        else:
            await self.send(text_data=json.dumps({
                "error": "There is an error in the message"
            }))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))

    def get_room_name(self, room_id):
        return Room.objects.get(id=room_id).room

    def get_room_pk(self, room_id):
        return Room.objects.get(id=room_id).pk

    def get_room_messages(self, room_pk):
        return Messages.objects.filter(room=room_pk)

    def serialize_messages(self, room_messages):
        serializer = MessagesSerializer(room_messages, many=True)
        return serializer.data

    def serializer_create_message(self, data):
        serializer = MessagesSerializer(data=data)
        if serializer.is_valid():
            print("Message saved")
            serializer.save()
            return serializer
        print(serializer.errors)
        return None
