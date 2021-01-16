import requests
import pytest
import json


@pytest.mark.parametrize("room_id", [i for i in range(1, 500)])
def test_get_bookings(room_id):
    """
    Tests if get_bookings request returns OK
    :param room_id: id of the room
    """
    url = "http://127.0.0.1:8000/get_bookings"

    #  Parameters for the request:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "room_id": room_id
    }
    #  Checks if requests returns OK:
    response = requests.get(url, params=data)
    assert response.status_code == 200


@pytest.mark.parametrize("sort_parameter", [i for i in ["price", "added_at"]])
def test_get_rooms(sort_parameter):
    sort_directions = ["ASC", "DESC"]
    url = "http://127.0.0.1:8000/get_rooms"
    for sort_direction in sort_directions:
        data = {
            "sort_parameter": sort_parameter,
            "sort_direction": sort_direction
        }
        response = requests.get(url, params=data)
        assert response.status_code == 200





