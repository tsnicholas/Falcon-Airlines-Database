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
    
def create_tables(connection : MySQLConnection, cursor : MySQLCursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS Passenger(\n'
                   '    passenger_id INT PRIMARY KEY AUTO_INCREMENT,\n'
                   '    Pname TEXT\n'
                   ');\n')
    connection.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS Airport(\n'
                   '    airport_id INT PRIMARY KEY AUTO_INCREMENT,\n'
                   '    alocation TEXT\n'
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

# To Do: Randomize this data.
def populate_tables(connection : MySQLConnection, cursor : MySQLCursor):
    cursor.execute("INSERT INTO Airport(alocation)\n"
                   "VALUES ('Indianapolis, IN'),\n"
                   "       ('Detriot, MI'),\n"
                   "       ('Chicago, IL'),\n"
                   "       ('Dallas, TX'),\n"
                   "       ('Dayton, OH');\n")
    connection.commit()
    cursor.execute("INSERT INTO Flight(takeoff, to_airport)\n"
                   "VALUES ('2023-04-18 12:00:00', 1),\n"
                   "       ('2023-04-19 05:00:00', 2),\n"
                   "       ('2023-04-23 13:30:00', 3),\n"
                   "       ('2023-04-10 07:45:00', 4),\n"
                   "       ('2023-04-20 04:20:00', 5);\n")
    connection.commit()
    cursor.execute("INSERT INTO Flight_Schedule(airport_id, flight_id)\n"
                   "VALUES (1, 4), (2, 5), (3, 4), (4, 2), (5, 1);\n")
    connection.commit()
    cursor.execute("INSERT INTO Passenger(Pname)\n"
                   "VALUES ('Jerry Smith'),\n"
                   "       ('Rick Sanchez'),\n"
                   "       ('Summer Smith'),\n"
                   "       ('Sponebob Squarepants'),\n"
                   "       ('Michael Bay'),\n"
                   "       ('Rin Tohsaka'),\n"
                   "       ('Miku Hatsune');\n")
    connection.commit()

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
        if choice.lower() == "a":
            processor.create_booking()
        elif choice.lower() == "b":
            processor.view_bookings()
        elif choice.lower() == "c":
            processor.delete_booking()
        else:
            print("Have a nice day!")
            break
        connection.commit()

if __name__ == '__main__':
    try:
        connection = create_connection()
        cursor = connection.cursor()
        create_tables(connection, cursor)
        populate_tables(connection, cursor)
        user_id = get_userId(connection, cursor)
        processor = bookingProcessor(cursor, user_id)
        main(connection, processor)
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(err)
