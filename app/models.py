from pydantic import BaseModel


class HotelRoom(BaseModel):
    """
    model of a hotel room
    includes description and price for a night
    """
    description: str  # text description of a room
    price: float  # price for a night


class Booking(BaseModel):
    """
    model of a booking of a room
    includes id of the room and dates for start and end
    """
    room_id: int
    start_date: str
    end_date: str
