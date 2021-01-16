import pytest
import requests
import json


@pytest.mark.parametrize("price", [i for i in range(2000, 3000)])
def test_add_room_request(price):
    """
    Tests if add_room requests returns OK
    :param price: price of the room
    """
    description = str(price - 2000 + 1) + " room"
    url = "http://127.0.0.1:8000/add_room"

    #  Parameters of the request:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "description": description,
        "price": price
    }
    #  Checks if request returns OK:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    assert response.status_code == 200


@pytest.mark.parametrize("room_id", [i for i in range(2, 500)])
def test_add_booking(room_id):
    """
    Tests if add_booking requests returns OK
    Adds 3 bookings for each room
    :param room_id: id of the room to book
    """
    #  Lists with dates:
    start_dates = ["2020-10-15", "2021-01-01", "2019-03-01"]
    end_dates = ["2020-10-20", "2021-01-10", "2019-04-21"]

    #  Checks if request returns OK:
    url = "http://127.0.0.1:8000/add_booking"
    for i in range(3):

        # Parameters for the request
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "room_id":  room_id,
            "start_date": start_dates[i],
            "end_date": end_dates[i]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        assert response.status_code == 200


