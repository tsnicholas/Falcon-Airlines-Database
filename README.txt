Developed by: Tim Nicholas <tsnicholas@bsu.edu>

Falcon Airlines is a fake airline database made to practice database programming in Connector/Python. 
The data seen from the program is randomly generated and will randomly generate data into the database each time it is ran.
In order to run this program, you must have python and mysql installed on your computer with a username and password.

How to install:
1. Download the executable file and the database.ini file.
2. Make sure both are present in the same folder, otherwise the program will crash upon executing.
3. Replace the username and password with your mysql's login information in database.ini using a text editor or IDE
4. Execute the program and follow the instructions.

Dependencies:
- Python 3
- MySQL
- database.ini (with your login information)

What I learned:
I learned that Python can interact with MySQL using pyconnection and can execute MySQL code within itself rather than having to make seperate MySQL scripts.
Perhaps it's much cleaner to make it into a seperate MySQL script that gets parsed, but it's still cool to see a programming language interacting with another one.
I also learned how to parse config files in order to enter the database. Using a config file might be helpful if I get serious about hiding sensitive information.

