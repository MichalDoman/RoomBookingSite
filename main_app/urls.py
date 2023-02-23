from django.urls import path
from .views import *

urlpatterns = [
    path('', Rooms.as_view(), name='rooms'),
    path('add-room', AddRoom.as_view(), name='add_room'),
    path('delete-room/<int:room_id>', DeleteRoom.as_view(), name='delete-room'),
]
