#inserting the basic info on the database
#this file is for the first time use only



import mysql.connector 

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "12345",

)

mydb.reset_session()

my_cursor = mydb.cursor()


my_cursor.execute(" DROP DATABASE Customers ") # comment this if you are executing this fill for the first time
mydb.commit()
my_cursor.execute(" CREATE DATABASE Customers ")
mydb.commit()

my_cursor.execute(" USE Customers ")
mydb.commit()

my_cursor.execute(f"""
CREATE TABLE customer(
    id INT AUTO_INCREMENT PRIMARY KEY,
    balance INT DEFAULT 0,
    username varchar(150) UNIQUE,
    password varchar(150),
    fullName varchar(150),
    Address varchar(150),
    Gender Boolean NOT NULL,
    maritalStatus varchar(150)
    )
""")

mydb.commit()

for i in range(5):
    username = f"{i}Jawad{i}"
    password = f"{i}12345"
    fullName = f"jawad{i}"
    address = "airportRoad"
    gender = 1 if i % 2 == 0 else 0  # 1 for True (Male), 0 for False (Female)
    maritalStatus = "single"

    my_cursor.execute(f"""INSERT INTO customer(username, password,fullName, Address, Gender, maritalStatus)  
                      
                      VALUES( '{username}', '{password}',  '{fullName}', '{address}', {gender}, '{maritalStatus}')
    """)
    mydb.commit()

for i in range(5):
    username = f"{i}Alex{i}"
    password = f"{i}12345"
    fullName = f"alex{i}"
    address = "sinelfil"
    gender = 1 if i % 2 == 0 else 0  # 1 for True (Male), 0 for False (Female)
    maritalStatus = "single"

    my_cursor.execute(f"""INSERT INTO customer(username, password ,fullName, Address, Gender, maritalStatus)  
                      
                      VALUES( '{username}', '{password}', '{fullName}', '{address}', {gender}, '{maritalStatus}')
    """)
    mydb.commit()


























