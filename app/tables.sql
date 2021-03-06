
-- TABLE with rooms

CREATE TABLE hotel_room (
    id INT PRIMARY KEY NOT NULL,
    description TEXT NOT NULL,
    price FLOAT NOT NULL,
    added_at TIMESTAMP

);

-- TABLE with bookings of roomsE

CREATE TABLE booking (
    id INT PRIMARY KEY NOT NULL,
    hotel_id INT NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotel_room(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);