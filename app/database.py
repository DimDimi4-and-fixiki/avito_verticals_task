from psycopg2 import connect
from models import HotelRoom, Booking


class DataBaseHandler(object):
    def __init__(self, **kwargs):
        self.connection = None
        self.create_connection()
        print(self.connection)

    def create_connection(self):
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
        cursor.execute(query)
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

    def get_last_id(self) -> int:
        #  SELECT query to the database:
        query = "SELECT MAX(id) FROM hotel_room"
        res = self.make_select_query(query=query)
        if not res[0][0]:
            return 0
        else:
            return int(res[0][0])

    def get_last_booking_id(self) -> int:
        #  SELECT query to the database:
        query = "SELECT MAX(id) FROM booking"
        res = self.make_select_query(query=query)
        if not res[0][0]:
            return 0
        else:
            return int(res[0][0])

    def get_current_timestamp(self) -> str:
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
        dict_room = room.dict()
        description = dict_room["description"]
        price = dict_room["price"]
        query = "SELECT * FROM hotel_room " \
                "WHERE description = \'{}\' " \
                "AND price = {}".format(description, price)
        res = self.make_select_query(query=query)
        room_id = int(res[0][0])
        return room_id

    def get_booking_id(self, booking: Booking) -> int:
        dict_booking = booking.dict()
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

    def add_room(self, room: HotelRoom) -> int:
        """
        Inserts a new hotel room into the database
        After the room is added returns an Id of it
        :param room: Hotel room to be added
        :return:
        """
        dict_room = room.dict()
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
        booking_dict = booking.dict()
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

    def add_booking(self, booking: Booking) -> int:
        booking_dict = booking.dict()
        room_id = booking_dict["room_id"]
        start_date = booking_dict["start_date"]
        end_date = booking_dict["end_date"]
        need_to_add = self.check_booking(booking=booking)
        if need_to_add:
            booking_id = int(self.get_last_booking_id()) + 1
            query = "INSERT INTO booking (id, hotel_id, start_date, end_date) " \
                    "VALUES ({}, {}, \'{}\', \'{}\')".format(booking_id, room_id, start_date, end_date)
            self.make_insert_query(query=query)
            return booking_id
        else:
            booking_id = self.get_booking_id(booking=booking)
            return booking_id

