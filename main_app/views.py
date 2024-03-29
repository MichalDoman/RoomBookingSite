from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime, date
from .models import Room, Reservation


class Rooms(View):
    """Room list view (home)"""
    def get(self, request):
        """Check room availability and display it. Sort displayed rooms according to sort_by url variable"""
        sort_by = request.GET.get('sort_by', 'pk')
        if 'availability' in sort_by:
            sort_by = 'pk'

        rooms = Room.objects.all().order_by(sort_by)
        reservations = Reservation.objects.all()

        # Check for room availability (False if room is not available today):
        date_now = datetime.today().strftime('%Y-%m-%d')
        rooms_tuple_list = []
        for room in rooms:
            availability = True
            for reservation in reservations:
                if room == reservation.room:
                    if str(date_now) == str(reservation.date):
                        availability = False
                        break
            rooms_tuple_list.append((room, availability))

        # sort by availability:
        if request.GET.get('sort_by') == 'availability':
            rooms_tuple_list.sort(key=lambda a: a[1])
        elif request.GET.get('sort_by') == '-availability':
            rooms_tuple_list.sort(key=lambda a: a[1], reverse=True)

        ctx = {'rooms': rooms_tuple_list}
        return render(request, 'rooms.html', ctx)


class AddRoom(View):
    """View for adding new rooms"""
    def get(self, request):
        """render proper template"""
        return render(request, 'add_room.html')

    def post(self, request):
        """create Room object with form data / display custom messages"""
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
    """Delete Room object on GET"""
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        room.delete()
        return redirect('/')


class ModifyRoom(View):
    def get(self, request, room_id):
        """render template with room modifying form"""
        room = Room.objects.get(pk=room_id)
        ctx = {'room': room}
        return render(request, 'modify_room.html', ctx)

    def post(self, request, room_id):
        """modify  existing room / display custom message"""
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


class RoomDetails(View):
    def get(self, request, room_id):
        """render template with room details"""
        room = Room.objects.get(pk=room_id)
        reservations = get_reservations(room_id)

        ctx = {'room': room,
               'reservations': reservations}
        return render(request, 'room_details.html', ctx)


class Reserve(View):
    """View for managing reservations"""
    def get(self, request, room_id):
        """render template for reserving rooms add current date to context to change
        display of expired reservations"""
        room = Room.objects.get(pk=room_id)
        date_now = datetime.today().strftime('%Y-%m-%d')
        reservations = get_reservations(room_id)

        ctx = {'room': room,
               'date_now': date_now,
               'reservations': reservations}
        return render(request, 'reserve.html', ctx)

    def post(self, request, room_id):
        """Reserve a room basing on the form data"""
        room = Room.objects.get(pk=room_id)
        date_now = datetime.today().strftime('%Y-%m-%d')
        comment = request.POST.get('comment')
        reservation_date = request.POST.get('reservation_date')

        message = 'Room reserved successfully!'
        message_color = '#38A83E'
        try:
            Reservation.objects.create(date=reservation_date, room=room, comment=comment)
        except IntegrityError:
            message = f"Room '{room.name}' is already reserved on {reservation_date}!"
            message_color = '#FF3E25'

        reservations = get_reservations(room_id)
        ctx = {'room': room,
               'date_now': date_now,
               'reservations': reservations,
               'message': message,
               'message_color': message_color}
        return render(request, 'reserve.html', ctx)


def get_reservations(room_id):
    """collects all the reservations done for a room. Checks whether any of them is already expired.

    :return a list of tuples. First element is a reservation,
    the other is a boolean that tells if the reservation is future or not."""

    room = Room.objects.get(pk=room_id)
    reservations = []

    for reservation in Reservation.objects.all().order_by('date'):
        expired = False
        if room == reservation.room:
            if reservation.date < date.today():
                expired = True
            reservations.append((reservation, expired))

    return reservations


class SearchRoom(View):
    """A separate View for searching for rooms"""
    def get(self, request):
        """render the template for searching rooms"""
        date_now = datetime.today().strftime('%Y-%m-%d')
        message = 'Searching results will be shown here.'
        ctx = {'date_now': date_now,
               'message': message}
        return render(request, 'search_room.html', ctx)

    def post(self, request):
        """display search results matching given filters."""
        date_now = datetime.today().strftime('%Y-%m-%d')
        availability_date = request.POST.get('availability_date')
        message = ''
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        has_projector = request.POST.get('has_projector')
        if has_projector:
            has_projector = True
        else:
            has_projector = False

        # Filter rooms:
        rooms = Room.objects.all().filter(name__icontains=name)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if has_projector:
            rooms = rooms.filter(has_projector=has_projector)
        # Check for availability:
        rooms_list = []
        reservations = Reservation.objects.all()
        for room in rooms:
            availability = True
            for reservation in reservations:
                if room == reservation.room:
                    if str(availability_date) == str(reservation.date):
                        availability = False
                        break
            if availability:
                rooms_list.append(room)

        if not rooms:
            message = "There are no rooms matching these requirements"

        ctx = {'rooms': rooms_list,
               'date_now': date_now,
               'message': message}
        return render(request, 'search_room.html', ctx)