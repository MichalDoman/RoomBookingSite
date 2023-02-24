from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
from .models import Room, Reservation


class Rooms(View):
    def get(self, request):
        rooms = Room.objects.all()
        reservations = Reservation.objects.all()

        # Check for room availability (False if room is not available today):
        date_now = datetime.today().strftime('%Y-%m-%d')
        rooms_tuple_list = []
        for room in rooms:
            availability = True
            for reservation in reservations:
                if room == reservation.room:
                    print(f'now: {date_now}')
                    print(reservation.date)
                    if str(date_now) == str(reservation.date):
                        availability = False
                        break
            rooms_tuple_list.append((room, availability))

        ctx = {'rooms': rooms_tuple_list}
        return render(request, 'rooms.html', ctx)


class AddRoom(View):
    def get(self, request):
        return render(request, 'add_room.html')

    def post(self, request):
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


class ModifyRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        ctx = {'room': room}
        return render(request, 'modify_room.html', ctx)

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        has_projector = request.POST.get('has_projector')

        room.name = name
        room.capacity = capacity
        if has_projector:
            room.has_projector = True
        else:
            room.has_projector = False

        message = 'New room information saved successfully!'
        message_color = '#38A83E'
        try:
            room.save()
        except IntegrityError:
            message = f"Room with name '{name}' already exists!"
            message_color = '#FF3E25'

        ctx = {'message': message, 'message_color': message_color}
        return render(request, 'modify_room.html', ctx)


class Reserve(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        ctx = {'room': room}
        return render(request, 'reserve.html', ctx)

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        comment = request.POST.get('comment')
        date = request.POST.get('reservation_date')

        message = 'Room reserved successfully!'
        message_color = '#38A83E'
        try:
            Reservation.objects.create(date=date, room=room, comment=comment)
        except IntegrityError:
            message = f"Room '{room.name}' is already reserved on {date}!"
            message_color = '#FF3E25'

        ctx = {'room': room, 'message': message, 'message_color': message_color}
        return render(request, 'reserve.html', ctx)
