from django.contrib import admin
from .models import *

admin.site.register(Room)
admin.site.register(RoomMember)
admin.site.register(Messages)
admin.site.register(RoomRequests)
