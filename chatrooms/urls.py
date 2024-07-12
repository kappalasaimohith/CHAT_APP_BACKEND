from django.urls import path
from .views import *

urlpatterns=[
    path('create_room/',CreateRoomView.as_view())
]