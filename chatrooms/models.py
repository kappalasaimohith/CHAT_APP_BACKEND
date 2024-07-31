from django.db import models
from user_auth.models import CustomUser
# Create your models here.
class Room(models.Model):
    # id = models.IntegerField(auto_created=True, primary_key=True)
    room = models.CharField(max_length=30, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.room

class Messages(models.Model):
    room= models.ForeignKey(Room, on_delete=models.CASCADE , related_name="messages")
    message = models.TextField()
    sent_by = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sent_by.username}: {self.message[:50]}'
    
class RoomMember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete= models.CASCADE)
    owner = models.BooleanField(default=False)
    member =models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
class RoomRequests(models.Model):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    PENDING  = 'pending'

    REQUEST_STATUS_CHOICES = (
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (PENDING, 'Pending')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=REQUEST_STATUS_CHOICES, default=PENDING)

    class Meta:
        verbose_name = 'Room Request'
        verbose_name_plural = 'Room Requests'

    def __str__(self):
        return f"Request by {self.user} for {self.room} - {self.status}"
