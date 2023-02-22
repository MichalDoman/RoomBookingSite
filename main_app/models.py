from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    has_projector = models.BooleanField()


class Reservation(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('date', 'room_id')
