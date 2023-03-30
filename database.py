import mysql.connector

def create_connection():
    return mysql.connector.connect(
        username = 'tsnicholas',
        password = 'Ptic43vr',
        host = 'localhost',
        database = 'falconAirlines'
    )

if __name__ == '__main__':
    try:
        connection = create_connection()
    except mysql.connector.Error as err:
        print(err.msg)
    finally:
        print("Connection Established!")
