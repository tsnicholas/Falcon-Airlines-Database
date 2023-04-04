import mysql.connector
from configparser import ConfigParser
from mysql.connector.connection import MySQLCursor 

passengerId : int

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

def create_connection() -> mysql.connector.connection.MySQLConnection:
    db_config = read_config_file('database.ini', 'mysql')
    print('Connecting to MySQL database...')
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        return conn
    else:
        raise mysql.connector.Error
    
def create_table(cursor : MySQLCursor):
    cursor.execute('DROP TABLE IF EXISTS Booking;\n')
    booking_table = ('CREATE TABLE Booking(\n'
                     '  booking_id INT PRIMARY KEY AUTO_INCREMENT,\n'
                     '  passenger_id INT,\n'
                     '  flight_id INT,\n'
                     '  CONSTRAINT PASSENGER_FK\n'
                     '  FOREIGN KEY (passenger_id) REFERENCES Passenger(passenger_id)\n'
                     '      ON DELETE SET NULL ON UPDATE CASCADE,\n'
                     '  CONSTRAINT BOOKED_FLIGHT_FK\n'
                     '  FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)\n'
                     '      ON DELETE SET NULL ON UPDATE CASCADE\n'
                     ');\n')
    cursor.execute(booking_table)

def main(cursor : MySQLCursor):
    while True:
        choice = input('Hello! What would you like to do?'
                       '    A. Create a booking.'
                       '    B. View a booking.'
                       '    C. Delete a booking.'
                       'Type another character to exit this menu.\n')
        if choice == "a":
            create_booking(cursor)
        else:
            print('Have a nice day!\n')
            break

def create_booking(cursor : MySQLCursor):
    flights = get_flights(cursor)
    print(f"Here are the current flights: \n{flights}")
    booking = input("Which flight would you like to book for? ")
    insert_booking(cursor, booking)

def get_flights(cursor : MySQLCursor) -> str:
    flights = ""
    cursor.execute('SELECT * FROM Flight;')
    for row in cursor.fetchall():
        flights + f'Flight id: {row[0]}, time: {row[1]}, to_airport: {row[3]}\n'
    return flights

def insert_booking(cursor : MySQLCursor, flight_booked : int):
    cursor.execute('INSERT INTO Booking(passenger_id, flight_id)'
                   f'VALUES (1, {flight_booked})')

if __name__ == '__main__':
    try:
        connection = create_connection()
    except mysql.connector.Error as err:
        print(err.msg)
    finally:
        cursor = connection.cursor()
        create_table(cursor)
        main(cursor)
        cursor.close()
        connection.close()
