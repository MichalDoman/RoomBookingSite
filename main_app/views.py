from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View
from .models import Room, Reservation


class Rooms(View):
    def get(self, request):
        rooms = Room.objects.all()
        reservations = Reservation.objects.all()
        reservations = [1]
        ctx = {'rooms': rooms,
               'reservations': reservations}
        return render(request, 'rooms.html', ctx)


class AddRoom(View):
    def get(self, request):
        return render(request, 'add_room.html')

    def post(self, request):
        rooms = Room.objects.all()
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        has_projector = request.POST.get('has_projector')
        if has_projector:
            has_projector = True
        else:
            has_projector = False

        message = 'Room added successfully!'
        message_color = '#38A83E'
        try:
            Room.objects.create(name=name, capacity=capacity, has_projector=has_projector)
        except IntegrityError:
            message = f"Room with name '{name}' already exists!"
            message_color = '#FF3E25'

        ctx = {'message': message, 'message_color': message_color}
        return render(request, 'add_room.html', ctx)


class DeleteRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        room.delete()
        return redirect('/')
