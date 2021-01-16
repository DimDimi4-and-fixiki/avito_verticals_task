import requests
import pytest
import json


@pytest.mark.parametrize("booking_id", [i for i in range(1, 200)])
def test_delete_booking(booking_id):
    """
    Tests if delete_bookings request returns OK
    :param booking_id: id of the booking
    """

    url = "http://127.0.0.1:8000/delete_booking"

    #  Parameters for the request:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "booking_id": booking_id
    }

    # Checks if delete_booking request returns OK:
    response = requests.post(url, params=data)
    assert response.status_code == 200


@pytest.mark.parametrize("room_id", [i for i in range(1, 500)])
def test_delete_room(room_id):
    """
    Tests if delete_room requests returns OK
    :param room_id: id of the room
    """

    url = "http://127.0.0.1:8000/delete_room"

    #  Parameters for the request:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "room_id": room_id
    }

    # Checks if delete_room request returns OK:
    response = requests.post(url, params=data)
    assert response.status_code == 200
