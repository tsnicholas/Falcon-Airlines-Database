import io
import random
import mysql.connector
from configparser import ConfigParser
from mysql.connector.connection import MySQLConnection
from mysql.connector.connection import MySQLCursor
from bookingProcessor import bookingProcessor

def read_config_file(filename : str, section : str):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in {filename}')
    return db

def create_connection() -> MySQLConnection:
    db_config = read_config_file('database.ini', 'mysql')
    print('Connecting to MySQL database...')
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        return conn
    else:
        raise mysql.connector.Error

def connect_to_database(connection : MySQLConnection, cursor : MySQLCursor):
    cursor.execute('CREATE DATABASE IF NOT EXISTS falconAirlines;')
    cursor.execute('USE falconAirlines;')
    connection.commit()

def create_tables(connection : MySQLConnection, cursor : MySQLCursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS Passenger(\n'
                   '    passenger_id INT PRIMARY KEY AUTO_INCREMENT,\n'
                   '    Pname TEXT\n'
                   ');\n')
    connection.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS Airport(\n'
                   '    airport_id INT PRIMARY KEY AUTO_INCREMENT,\n'
                   '    alocation VARCHAR(225) UNIQUE\n'
                   ');\n')
    connection.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS Flight(\n'
                   '    flight_id INT PRIMARY KEY AUTO_INCREMENT,\n'
                   '    takeoff DATETIME,\n'
                   '    to_airport INT,\n'
                   '    CONSTRAINT destinationairport_fk\n'
                   '    FOREIGN KEY (to_airport) REFERENCES Airport(airport_id)\n'
                   '        ON DELETE SET NULL ON UPDATE CASCADE\n'
                   ');\n')
    connection.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS Flight_Schedule(\n'
                   '    airport_id INT,\n'
                   '    flight_id INT,\n'
                   '    CONSTRAINT airport_fk\n'
                   '    FOREIGN KEY (airport_id) REFERENCES Airport(airport_id)\n'
                   '        ON DELETE SET NULL ON UPDATE CASCADE,\n'
                   '    CONSTRAINT flight_fk\n'
                   '    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)\n'
                   '        ON DELETE SET NULL ON UPDATE CASCADE\n'
                   ');\n')
    connection.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS Booking(\n'
                   '    booking_id INT PRIMARY KEY AUTO_INCREMENT,\n'
                   '    passenger_id INT,\n'
                   '    flight_id INT,\n'
                   '    CONSTRAINT passenger_fk\n'
                   '    FOREIGN KEY (passenger_id) REFERENCES Passenger(passenger_id)\n'
                   '        ON DELETE SET NULL ON UPDATE CASCADE,\n'
                   '    CONSTRAINT booked_flight_fk\n'
                   '    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)\n'
                   '        ON DELETE SET NULL ON UPDATE CASCADE\n'
                   ');\n')
    connection.commit()

def populate_tables(connection : MySQLConnection, cursor : MySQLCursor):
    cursor.execute("INSERT INTO Airport(alocation)\n"
                   "VALUES ('Indianapolis, IN'), ('Detriot, MI'), ('Chicago, IL'), ('Dallas, TX'), ('Dayton, OH'), \n"
                   "       ('New York, NY'), ('Miami, FL'), ('Las Vegas, NV'), ('San Francisco, CA'), ('Nashville, TN'),\n"
                   "       ('Salt Lake City, UT'), ('Denver, CO'), ('Philadelphia, PA'), ('Springfield, OR')\n"
                   "            ON DUPLICATE KEY UPDATE alocation = alocation;\n")
    connection.commit()
    # We want to make sure the number doesn't exceed the amount of airports in randomizing the destination's id
    cursor.execute("SELECT COUNT(airport_id) FROM Airport;")
    num_of_airports = int(cursor.fetchall()[0][0])
    cursor.execute(randomize_flights(num_of_airports))
    connection.commit()
    # We want the most recent flight ids and use them in order. 
    # Otherwise, a flight can come from more than one airport, which is impossible.
    cursor.execute("SELECT flight_id\nFROM Flight\nORDER BY flight_id DESC LIMIT 5;\n")
    new_flight_ids = cursor.fetchall()
    cursor.execute(randomize_schedule(num_of_airports, new_flight_ids))
    connection.commit()

def randomize_flights(num_of_airports : int) -> str:
    prompt = io.StringIO()
    prompt.write("INSERT INTO Flight(takeoff, to_airport)\nVALUES ")
    for i in range(num_of_airports):
        prompt.write(f"('2023-04-{random.randrange(1, 31)} {random.randrange(6, 18)}:00:00', {random.randrange(1, num_of_airports)}),\n")
    temp = prompt.getvalue()
    return f"{temp[0:len(temp) - 2]};\n"

def randomize_schedule(num_of_airports : int, new_flight_ids) -> str:
    prompt = io.StringIO()
    prompt.write("INSERT INTO Flight_Schedule(airport_id, flight_id)\nVALUES ")
    for row in new_flight_ids:
        prompt.write(f"({random.randrange(1, num_of_airports)}, {row[0]}),\n")
    temp = prompt.getvalue()
    return f"{temp[0:len(temp) - 2]};\n"

def get_userId(connection : MySQLConnection, cursor : MySQLCursor) -> int:
    name = input("What's your first and last name? ")
    cursor.execute(f"SELECT passenger_id FROM Passenger WHERE Pname = '{name}';")
    result = cursor.fetchall()
    if len(result) == 0:
        print("Adding your name into the database...")
        result = add_new_passenger(name, connection, cursor)
    return result[0][0]

def add_new_passenger(name : str, connection : MySQLConnection, cursor : MySQLCursor):
    cursor.execute('INSERT INTO Passenger (Pname)\n'
                   f"VALUES ('{name}');\n")
    connection.commit()
    cursor.execute(f"SELECT passenger_id FROM Passenger WHERE Pname = '{name}';")
    return cursor.fetchall()
    

def main(connection : MySQLConnection, processor : bookingProcessor):
    while True:
        choice = input('What would you like to do?\n'
                       '    A. Create a booking.\n'
                       '    B. View your bookings.\n'
                       '    C. Delete a booking.\n'
                       'Type another character to exit this menu.\n')
        match choice.lower():
            case "a":
                processor.create_booking()
            case "b":
                processor.view_bookings()
            case "c":
                processor.delete_booking()
            case _:
                print("Have a nice day!")
                break
        connection.commit()

if __name__ == '__main__':
    try:
        connection = create_connection()
        cursor = connection.cursor()
        connect_to_database(connection, cursor)
        create_tables(connection, cursor)
        populate_tables(connection, cursor)
        user_id = get_userId(connection, cursor)
        processor = bookingProcessor(cursor, user_id)
        main(connection, processor)
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(err)
