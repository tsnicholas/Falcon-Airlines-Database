USE falconAirlines;

INSERT INTO Airport(alocation)
VALUES ('Indianapolis, IN'),
       ('Detroit, MI'),
       ('Chicago, IL'),
       ('Dallas, TX'),
       ('New York, NY'),
       ('Miami, FL'),
       ('Las Vegas, NV'),
       ('San Francisco, CA'),
       ('Dayton, OH');

INSERT INTO Flight(takeoff, to_airport)
VALUES ('2023-04-18 12:00:00', 1),
       ('2023-04-19 05:00:00', 2),
       ('2023-04-23 13:30:00', 3),
       ('2023-04-10 07:45:00', 4),
       ('2023-04-20 04:20:00', 5),
       ('2023-04-08 16:30:00', 6),
       ('2023-04-13 18:45:00', 7),
       ('2023-04-14 14:30:00', 8),
       ('2023-04-15 06:00:00', 9);

INSERT INTO Flight_Schedule(airport_id, flight_id)
VALUES (1, 9), (2, 3), (4, 4), (5, 6), (3, 7), (6, 1), (7, 2), 
       (8, 5), (9, 8);

INSERT INTO Passenger(Pname)
VALUES ('Jerry Smith'),
       ('Timothy Nicholas'),
       ('Michael Bay'),
       ('Rick Sanchez'),
       ('Spongebob Squarepants'),
       ('Rin Tohsaka'),
       ('Sally Jones'),
       ('Summer Smith');
       