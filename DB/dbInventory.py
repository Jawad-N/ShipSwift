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


my_cursor.execute("DROP DATABASE Inventory") # comment this if you are executing this fill for the first time
mydb.commit()
my_cursor.execute("CREATE DATABASE Inventory")
mydb.commit()

my_cursor.execute("USE Inventory")
mydb.commit()

my_cursor.execute(f"""
CREATE TABLE customer(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name varchar(150) NOT NULL,
    category varchar(150) NOT NULL,
    price INT NOT NULL,
    description varchar(150)
    )
""")

mydb.commit()

for i in range(10):
    name = "spirto"
    category = "cleaning"
    price = 50
    description = "binadif"
    my_cursor.execute(f"""
        INSERT INTO customer(name, category, price, description)  
        VALUES('{name}', '{category}', '{price}' , '{description}')
    """)
    mydb.commit()

for i in range(10):
    name = "water Bottle"
    category = "equipment"
    price = 100
    description = "aninet may murex"
    my_cursor.execute(f"""
        INSERT INTO customer(name, category, price, description)  
        VALUES('{name}', '{category}', '{price}' , '{description}')
    """)
    mydb.commit()
























