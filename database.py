import mysql.connector
from configparser import ConfigParser

def read_config_file(filename, section):
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

def create_connection():
    db_config = read_config_file('database.ini', 'mysql')
    print('Connecting to MySQL database...')
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        return conn
    else:
        raise mysql.connector.Error

if __name__ == '__main__':
    try:
        connection = create_connection()
    except mysql.connector.Error as err:
        print(err.msg)
    finally:
        print("Connection Established!")
