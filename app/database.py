from psycopg2 import connect
from models import HotelRoom, Booking
from dates import DateHandler


class DataBaseHandler(object):
    """"
    Class to handle all the operations with PostgreSQL DB
    """
    def __init__(self, **kwargs):
        self.connection = None
        self.create_connection()
        print(self.connection)

    def create_connection(self):
        """
        Sets connection with the database
        """

        # MY PARAMETERS OF THE DATABASE:
        self.connection = connect(
            user="avito",
            host="localhost",
            database="avito_backend",
            password="Stepler32"
        )

    def make_select_query(self, query: str) -> list:
        """
        makes a SELECT query to the database and returns rows
        :param query:  query text
        :return: rows
        """
        print(query)
        self.create_connection()  # sets connection
        cursor = self.connection.cursor()  # cursor to execute the query
        cursor.execute(query)  # Executes the query
        rows = cursor.fetchall()  # result of the query
        return rows

    def make_insert_query(self, query: str):
        """
        makes an INSERT query to the database
        commits changes to the database
        :param query: query text
        """

        print(query)
        self.create_connection()  # sets connection
        cursor = self.connection.cursor()  # cursor to perform the query
        res = cursor.execute(query)  # result of the query
        self.connection.commit()  # commits changes

    def make_update_query(self, query: str):
        """
        makes an UPDATE query to the database
        commits changes to the database
        :param query: query text
        """

        self.create_connection()  # sets connection
        cursor = self.connection.cursor()  # cursor to execute the query
        res = cursor.execute(query)  # result of the query
        self.connection.commit()  # commits changes

    def make_delete_query(self, query: str):
        """
        makes a DELETE query to the database
        commits changes to the database
        :param query: query text
        """

        self.create_connection()  # sets connection
        cursor = self.connection.cursor()  # cursor to execute the query
        res = cursor.execute(query)  # result of the query
        self.connection.commit()  # commits changes

    def get_last_id(self) -> int:
        #  SELECT query to the database:
        query = "SELECT MAX(id) FROM hotel_room"
        res = self.make_select_query(query=query)
        if not res[0][0]:  # Rooms table is empty
            return 0
        else:
            return int(res[0][0])

    def get_last_booking_id(self) -> int:
        #  SELECT query to the database:
        query = "SELECT MAX(id) FROM booking"
        res = self.make_select_query(query=query)
        if not res[0][0]:  # Bookings table is empty
            return 0
        else:
            return int(res[0][0])

    def get_current_timestamp(self) -> str:
        """
        Returns current DATE TIME (Timestamp)
        :return: str object with a timestamp
        """

        # SELECT query:
        query = "SELECT CURRENT_TIMESTAMP"
        res = self.make_select_query(query=query)
        return str(res[0][0])

    def get_room_id(self, room: HotelRoom) -> int:
        """
        Gets id of the room
        :param room: hotel room from the database
        :return: id of the room
        """

        # SELECT query to the database
        dict_room = room.dict()  # dictionary with the room info
        description = dict_room["description"]
        price = dict_room["price"]
        query = "SELECT * FROM hotel_room " \
                "WHERE description = \'{}\' " \
                "AND price = {}".format(description, price)
        res = self.make_select_query(query=query)
        room_id = int(res[0][0])
        return room_id

    def get_booking_id(self, booking: Booking) -> int:
        dict_booking = booking.dict()  # dictionary with the room info
        room_id = dict_booking["room_id"]
        start_date = dict_booking["start_date"]
        end_date = dict_booking["end_date"]
        #  SELECT query to the database:
        query = "SELECT * FROM booking " \
                "WHERE hotel_id = {} " \
                "AND start_date = \'{}\' " \
                "AND end_date = \'{}\'".format(room_id, start_date, end_date)
        res = self.make_select_query(query=query)
        booking_id = int(res[0][0])
        return booking_id

    def check_room_by_id(self, room_id) -> bool:
        """
        Checks if room in the database
        :param room_id: id of the room
        :return: True if room exists; False if not
        """

        # SELECT query to the database:
        query = "SELECT * FROM hotel_room " \
                "WHERE id = {}".format(str(room_id))
        res = self.make_select_query(query=query)
        return not res == []

    def check_booking_by_id(self, booking_id) -> bool:
        """
        Checks if booking is in the database
        :param booking_id: id of the booking
        :return: True if booking is in the database; False if not
        """

        #  SELECT query to the database:
        query = "SELECT * FROM booking " \
                "WHERE id = {}".format(booking_id)
        res = self.make_select_query(query=query)
        return not res == []

    def check_room(self, room: HotelRoom):
        """
        Checks if room can be added
        :param: room - a hotel room to check
        :return: True if room can be added
        :return: False if room cannot be added
        """
        dict_room = room.dict()  # room in a dictionary
        description = str(dict_room["description"])
        price = str(dict_room["price"])

        # SELECT query to the database:
        query = "SELECT * FROM hotel_room " \
                "WHERE description = \'{}\' " \
                "AND price = {}".format(description, price)
        res = self.make_select_query(query=query)
        return res == []  # if res is empty returns True

    def get_all_rooms(self):
        query = "SELECT * FROM hotel_room"
        res = self.make_select_query(query=query)
        return res

    def get_all_rooms_sorted(self, sort_parameter, sort_direction="ASC"):
        """
        Gets list of rooms ordered by parameter
        :param sort_parameter: parameter to sort by
        :param sort_direction: direction to order by
        :return: list of all rooms
        """
        query = "SELECT * FROM hotel_room " \
                "ORDER BY {} {}".format(sort_parameter, sort_direction)
        res = self.make_select_query(query=query)
        return res

    def add_room(self, room: HotelRoom) -> int:
        """
        Inserts a new hotel room into the database
        After the room is added returns an Id of it
        :param room: Hotel room to be added
        :return:
        """
        dict_room = room.dict()  # Room in a dictionary
        description = str(dict_room["description"])
        price = str(dict_room["price"])
        need_to_add = self.check_room(room)  # add or not to
        added_at = self.get_current_timestamp()

        if need_to_add:
            # INSERT query to the database:
            room_id = self.get_last_id() + 1
            query = "INSERT INTO hotel_room (id, description, price, added_at) " \
                    "VALUES ({}, \'{}\', {}, \'{}\')".format(
                        room_id, description, price, added_at)
            self.make_insert_query(query)
            return room_id
        else:
            #  Gets id of the room:
            room_id = self.get_room_id(room=room)
            return room_id

    def check_booking(self, booking: Booking):
        booking_dict = booking.dict()  # Booking in a dictionary
        room_id = booking_dict["room_id"]
        start_date = booking_dict["start_date"]
        end_date = booking_dict["end_date"]

        #  SELECT query to the database:
        query = "SELECT * FROM booking " \
                "WHERE hotel_id = {} " \
                "AND start_date = \'{}\' " \
                "AND end_date = \'{}\'".format(room_id, start_date, end_date)
        res = self.make_select_query(query=query)
        return res == []

    def add_booking(self, booking: Booking):
        date_handler = DateHandler()
        booking_dict = booking.dict()  # dictionary with the booking
        room_id = booking_dict["room_id"]  # id of the room
        start_date = booking_dict["start_date"]  # date of start
        end_date = booking_dict["end_date"]  # date of the end

        #  Checks dates:
        if not date_handler.check_date(date=start_date):
            return "Start date is not valid"
        if not date_handler.check_date(date=end_date):
            return "End date is not valid"

        #  Checks if booking is needed to be added:
        need_to_add = self.check_booking(booking=booking)  # flag

        #  Checks if room exists:
        room_exists = self.check_room_by_id(room_id=room_id)

        if not room_exists:  # The room is not in the table
            return "No such room"

        # (add or not to add)
        if need_to_add:
            #  Adds new booking:
            booking_id = int(self.get_last_booking_id()) + 1
            query = "INSERT INTO booking (id, hotel_id, start_date, end_date) " \
                    "VALUES ({}, {}, \'{}\', \'{}\')".format(booking_id, room_id, start_date, end_date)
            self.make_insert_query(query=query)
            return booking_id
        else:
            # Returns id of existing booking:
            booking_id = self.get_booking_id(booking=booking)
            return booking_id

    def get_rooms(self, sort_parameter=None, sort_direction=None) -> list:
        """
        Gets list of rooms sorted by parameter in a direction (acs/desc)
        :param sort_parameter: parameter to ORDER BY
        :param sort_direction: direction to sort (ASC/DESC)
        :return: list of rooms
        """
        if not sort_parameter:  # parameter is not defined
            res = self.get_all_rooms()  # All rooms from the database
        else:
            #  Gets ordered rooms:
            res = self.get_all_rooms_sorted(sort_parameter=sort_parameter,
                                            sort_direction=sort_direction)
        ans = []  # list to return
        for room in res:
            d = {  # dictionary with the room
                "room_id": room[0],
                "description": room[1],
                "price": room[2],
                "added_at": room[3]
            }
            ans.append(d)  # Adds room to the list
        return ans

    def get_bookings(self, room_id: int) -> list:
        """
        Gets list of booking for a room
        :param room_id: id of the room
        :return: bookings sorted by start date
        """
        query = "SELECT * FROM booking " \
                "WHERE hotel_id = {} " \
                "ORDER BY start_date".format(room_id)
        res = self.make_select_query(query=query)
        ans = []  # list to return
        for booking in res:
            d = {  # dictionary with a booking
                "booking_id": booking[0],
                "start_date": booking[2],
                "end_date": booking[3]
            }
            ans.append(d)  # adds booking
        return ans

    def delete_booking(self, booking_id: int):
        """
        Deletes booking of a room by its id
        :param booking_id: id of the booking
        """

        # Checks if booking is in the database:
        booking_exists = self.check_booking_by_id(booking_id=booking_id)
        if not booking_exists:
            return "No such booking"
        # DELETE query to the database:
        query = "DELETE FROM booking " \
                "WHERE id = {}".format(booking_id)
        self.make_delete_query(query=query)

    def delete_bookings_by_room_id(self, room_id: int):
        """
        Deletes all bookings of a room by room's id
        :param room_id: id of the room
        """

        # DELETE query to the database:
        query = "DELETE FROM booking " \
                "WHERE hotel_id = {}".format(room_id)
        self.make_delete_query(query=query)

    def delete_room(self, room_id: int):
        """
        Deletes room and the bookings of it
        :param room_id: id of the room
        """

        #  Checks if room is in the database:
        room_exists = self.check_room_by_id(room_id=room_id)
        if not room_exists:  # Room is not in the table
            return "No such room"

        # Firstly, delete all bookings:
        self.delete_bookings_by_room_id(room_id=room_id)

        # Delete record of the room from the table:
        query = "DELETE FROM hotel_room " \
                "WHERE id = {}".format(room_id)

        self.make_delete_query(query=query)

