# RoomBookingWebsite

### About app:
This app was made as part of a workshop exercises on  my course. It was my first "polished" Django app. Its main purpose was to manage rooms and their reservations. It uses PostgreSQL to manage datasets. Below there is a brief showcase of the Views:

### Home View:
On Home View there is a sortable list of all the rooms and their details. Every room can be edited, reserved or deleted with the click of the icons. Main tabs lead to search view and room adding view.
<p align="center">
    <img src="https://github.com/MichalDoman/RoomBookingWebsite/blob/main/screenshots/room_list.png"  width="70%" height="30%">
</p>

### Search View:
In this view after filling the form, a list of filtered rooms id displayed. rooms can be filtered by name, capacity, date or availability of the projector.
<p align="center">
    <img src="https://github.com/MichalDoman/RoomBookingWebsite/blob/main/screenshots/search_view.png"  width="70%" height="30%">
</p>

### Adding Room:
In this view there is just a form that after being submitted, creates new room that is automatically added to the main page. A room cannot be added if its name is already taken.
<p align="center">
    <img src="https://github.com/MichalDoman/RoomBookingWebsite/blob/main/screenshots/add_room.png"  width="70%" height="30%">
</p>

### Reserving rooms:
In this view a reservation can be added to a room. It cannot be added when a room is already taken at a specific date. Reservations can be described with a note.
<p align="center">
    <img src="https://github.com/MichalDoman/RoomBookingWebsite/blob/main/screenshots/reserve_view.png"  width="70%" height="30%">
</p>

