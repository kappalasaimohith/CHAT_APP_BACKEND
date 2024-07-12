from django.db import models
from user_auth.models import CustomUser
# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=30, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.room_name

class Messages(models.Model):
    room_name= models.ForeignKey(Room, on_delete=models.CASCADE , related_name="messages")
    message = models.TextField()
    sent_by = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sent_by.username}: {self.message[:50]}'