from django.urls import re_path
from .consumers import AsyncChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/(?P<id>[^/]+)/$', AsyncChatConsumer.as_asgi()),
    # re_path(r'^ws/text_consumer/', TextRoomConsumer.as_asgi()),
]