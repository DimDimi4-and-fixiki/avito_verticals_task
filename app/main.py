from fastapi import FastAPI
from models import HotelRoom, Booking
from database import DataBaseHandler

app = FastAPI()  # API object
database_handler = DataBaseHandler()  # handler to work with the database


@app.get("/")
def check_app():  # checks that API works
    return {"message": "It works fine :)"}


@app.post("/add_room")
def add_room(room: HotelRoom):
    """
    Handles 'add_room' request
    :param room: HotelRoom object
    :return: id of the room
    """
    room_id = database_handler.add_room(room=room)
    return {"id": room_id}


@app.get("/get_rooms")
def get_rooms(sort_parameter=None, sort_direction=None):
    """
    Handles 'get_rooms' request
    :param sort_parameter: parameter to sort by
    :param sort_direction: direction to sort with
    :return: list of rooms
    """
    res = database_handler.get_rooms(sort_parameter=sort_parameter,
                                     sort_direction=sort_direction)
    return res


@app.post("/add_booking")
def add_booking(booking: Booking):
    """
    Handles add_booking request
    :param booking: booking object to add
    :return: id of the booking
    """
    booking_id = database_handler.add_booking(booking=booking)
    if booking_id == "No such room":
        return {"error": booking_id}
    if booking_id in ["Start date is not valid", "End date is not valid"]:
        return {"error": booking_id}
    else:
        return {"id": booking_id}


@app.get("/get_bookings")
def get_bookings(room_id: int):
    """
    Handles get_bookings request
    :param room_id: id of the room
    :return: list of all bookings for the room
    """
    res = database_handler.get_bookings(room_id=room_id)
    return res  # list of bookings


@app.post("/delete_room")
def delete_room(room_id: int):
    """
    Handles delete_room request
    Deletes the room and all bookings of it
    :param room_id: id of the room
    """
    res = database_handler.delete_room(room_id=room_id)
    if res == "No such room":
        return {"error": res}


@app.post("/delete_booking")
def delete_booking(booking_id: int):
    """
    Handles delete_booking event
    :param booking_id: id of the booking
    Deletes all information about the booking
    """
    res = database_handler.delete_booking(booking_id=booking_id)
    if res == "No such booking":
        return {"error": res}