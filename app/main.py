from fastapi import FastAPI
from models import HotelRoom, Booking
from database import DataBaseHandler

app = FastAPI()
database_handler = DataBaseHandler()


@app.get("/")
def check_app():
    return {"message": "It works fine :)"}


@app.get("/get_all_rooms")
def get_all_rooms():
    rooms = database_handler.get_all_rooms()
    return {"res": rooms}


@app.post("/add_room")
def add_room(room: HotelRoom):
    room_id = database_handler.add_room(room=room)
    return {"id": room_id}


@app.get("/get_rooms")
def get_rooms(sort_parameter=None, sort_direction=None):
    res = database_handler.get_rooms(sort_parameter=sort_parameter,
                                     sort_direction=sort_direction)
    return res


@app.post("/add_booking")
def add_booking(booking: Booking):
    booking_id = database_handler.add_booking(booking=booking)
    return {"id": booking_id}


@app.get("/get_bookings")
def get_bookings(room_id: int):
    res = database_handler.get_bookings(room_id=room_id)
    return res


@app.post("/delete_room")
def delete_room(room_id: int):
    database_handler.delete_room(room_id=room_id)


@app.post("/delete_booking")
def delete_booking(booking_id: int):
    database_handler.delete_booking(booking_id=booking_id)