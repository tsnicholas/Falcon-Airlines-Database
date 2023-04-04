DROP DATABASE IF EXISTS falconAirlines;
CREATE DATABASE falconAirlines;
USE falconAirlines;

CREATE TABLE Passenger(
    passenger_id INT PRIMARY KEY AUTO_INCREMENT,
    Pname TEXT
);

CREATE TABLE Airport(
    airport_id INT PRIMARY KEY AUTO_INCREMENT,
    alocation TEXT
);

CREATE TABLE Flight(
    flight_id INT PRIMARY KEY AUTO_INCREMENT,
    takeoff DATETIME,
    to_airport INT,
    CONSTRAINT destinationairport_fk
    FOREIGN KEY (to_airport) REFERENCES Airport(airport_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE Flight_Schedule(
    airport_id INT,
    flight_id INT,
    CONSTRAINT airport_fk
    FOREIGN KEY (airport_id) REFERENCES Airport(airport_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT flight_fk
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);
