from django.urls import path
from .views import *

urlpatterns = [
    path('', Rooms.as_view(), name='rooms'),
    path('add-room', AddRoom.as_view(), name='add_room'),
    path('delete-room/<int:room_id>', DeleteRoom.as_view(), name='delete_room'),
    path('modify-room/<int:room_id>', ModifyRoom.as_view(), name='modify_room'),
    path('reserve/<int:room_id>', Reserve.as_view(), name='reserve'),
    path('room-details/<int:room_id>', RoomDetails.as_view(), name='room_details'),
    path('search-room', SearchRoom.as_view(), name='search_room'),
]
