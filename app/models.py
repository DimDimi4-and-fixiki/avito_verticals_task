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
    room_id: int  # Id of the room
    start_date: str  # Date of start
    end_date: str  # Date of the end
