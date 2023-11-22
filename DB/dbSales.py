#inserting the basic info on the database
# running this file will generate a db with tables : user, room, reservation
# and fill up the room table with 15 instances 5 single, 5 double, and 5 suitess
import mysql.connector 

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "12345",

)

mydb.reset_session()

my_cursor = mydb.cursor()


my_cursor.execute(" DROP DATABASE Sales ") # comment this if you are executing this fill for the first time
mydb.commit()
my_cursor.execute(" CREATE DATABASE Sales ")
mydb.commit()

my_cursor.execute(f"""
CREATE TABLE customer(
    id INT AUTO_INCREMENT PRIMARY KEY,
    email varchar(150) UNIQUE,
    password varchar(150),
    fullName varchar(150),
    Address varchar(150),
    Gender Boolean NOT NULL,
    maritalStatus varchar(150)
    )
""")

mydb.commit()























