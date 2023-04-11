from mysql.connector.connection import MySQLCursor

class bookingProcessor:
    def __init__(self, cursor : MySQLCursor, user_id : int):
        self.cursor = cursor
        self.user_id = user_id

    def create_booking(self):
        flight_ids = self.get_flight_ids()
        print(f"Here are the current flights: \n")
        self.print_flights()
        while True:
            try:
                booking = int(input("Which flight would you like to book for? "))
                if booking == -1:
                    print("Booking Cancelled.\n")
                    break
                elif booking in flight_ids:
                    self.insert_booking(booking)
                    print("Booking successfully created!\n")
                    break
                else:
                    print('Not a valid flight id. Please try again or type "-1" to cancel.\n')
            except ValueError:
                print('Not an integer. Please try again or type "-1" to cancel.\n')

    def get_flight_ids(self) -> list[int]:
        ids = []
        self.cursor.execute('SELECT flight_id FROM Flight;')
        for row in self.cursor.fetchall():
            ids.append(row[0])
        return ids
    
    def print_flights(self):
        self.cursor.execute('SELECT F.flight_id, alocation, takeoff, (SELECT alocation FROM Airport WHERE to_airport = airport_id)\n' 
                            'FROM Flight AS F JOIN Flight_Schedule USING (flight_id) JOIN Airport USING (airport_id);')
        for row in self.cursor.fetchall():
            print(f"Id: {row[0]}, Location: {row[1]}, Destination: {row[3]}, Date and Time: {row[2]}")

    def insert_booking(self, flight_booked : int):
        self.cursor.execute('INSERT INTO Booking(passenger_id, flight_id)'
                           f'VALUES ({self.user_id}, {flight_booked})')

    def view_bookings(self):
        self.cursor.execute('SELECT booking_id, alocation, takeoff, (SELECT alocation FROM Airport WHERE to_airport = airport_id)\n'
                            'FROM Booking JOIN Flight USING (flight_id) JOIN Flight_Schedule USING (flight_id) JOIN Airport USING (airport_id)\n'
                            f'WHERE passenger_id = {self.user_id};')
        for row in self.cursor.fetchall():
            print(f"Booking Id: {row[0]}, Location: {row[1]}, Destination: {row[3]}, Date and Time: {row[2]}")
        print("\n")

    def delete_booking(self):
        user_bookings = self.get_booking_ids()
        if(len(user_bookings) == 0):
            print("You have no bookings to delete.")
            return
        while True:
            try:
                booking = int(input("What's the id of the booking you would like to delete? "))
                if booking == -1:
                    print("Deletion cancelled.\n")
                    break
                elif booking in user_bookings[0]:
                    self.cursor.execute(f'DELETE FROM Booking WHERE Booking_id = {booking}')
                    print('Booking successfully deleted.\n')
                    break
                else:
                    print('Not a valid id. Please try again or type "-1" to cancel.')
            except ValueError:
                print('Not an integer. Please try again or type "-1" to cancel.')

    def get_booking_ids(self):
        self.cursor.execute(f'SELECT booking_id FROM Booking WHERE passenger_id = {self.user_id}')
        return self.cursor.fetchall()
