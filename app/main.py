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


@app.post("/add_booking")
def add_booking(booking: Booking):
    booking_id = database_handler.add_booking(booking=booking)
    return {"id": booking_id}
