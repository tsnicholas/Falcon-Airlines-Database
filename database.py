import mysql.connector
from configparser import ConfigParser
from mysql.connector.connection import MySQLCursor
from mysql.connector.connection import MySQLConnection

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

def main(connection : MySQLConnection, cursor : MySQLCursor):
    while True:
        choice = input('What would you like to do?\n'
                       '    A. Create a booking.\n'
                       '    B. View a booking.\n'
                       '    C. Delete a booking.\n'
                       'Type another character to exit this menu.\n')
        if choice == "a":
            create_booking(cursor)
        else:
            print('Have a nice day!\n')
            break
        connection.commit()

def create_booking(cursor : MySQLCursor):
    flight_ids = get_flight_ids(cursor)
    print(flight_ids)
    print(f"Here are the current flights: \n")
    print_flights(cursor)
    while True:
        booking = input("Which flight would you like to book for? ")
        if int(booking) in flight_ids:
            insert_booking(cursor, booking)
            break
        else:
            print("Not a valid flight id. Please try again.\n")
    print("Booking successfully created!\n")

def get_flight_ids(cursor: MySQLCursor) -> list[int]:
    ids = []
    cursor.execute('SELECT flight_id FROM Flight;')
    for row in cursor.fetchall():
        ids.append(row[0])
    return ids
    
def print_flights(cursor : MySQLCursor):
    cursor.execute('SELECT flight_id, alocation, takeoff, (SELECT alocation FROM Airport WHERE to_airport = airport_id)\n' 
                   'FROM Flight JOIN Flight_Schedule USING (flight_id) JOIN Airport USING (airport_id);')
    for row in cursor.fetchall():
        print(f"Id: {row[0]}, Location: {row[1]}, Destination: {row[3]}, Date and Time: {row[2]}")

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
        main(connection, cursor)
        cursor.close()
        connection.close()
