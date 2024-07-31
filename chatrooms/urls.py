from django.urls import path
from .views import *

urlpatterns=[
    path('rooms/',CreateRoomView.as_view()),
    path('room/get_messages/<str:id>/',GetMessages.as_view()),
    path('join_room/', RoomsToJoinView.as_view()),
    path('my_requests/', GetMyRequests.as_view()),
    path('other_requests/', GetOtherRequests.as_view()),
    path('get_messages/<str:id>/',ViewMessages.as_view()),
    path('get_all_rooms/',GetAllEligibleRooms.as_view()),
]