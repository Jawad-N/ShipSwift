import mysql.connector 

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    passwd = "12345",
    port = 3307
)


mydb.reset_session()
my_cursor = mydb.cursor()
my_cursor.execute("USE DB")
mydb.commit()
##################################################### functions that control customer db



### Add customer to DB
def registerCustomer(username, password, fullName, address, gender, maritalStatus, wallet):
    try:
        my_cursor.execute(f"""INSERT INTO customer(username, password, fullName, Address, Gender, maritalStatus, wallet)  
                        VALUES( '{username}', '{password}',  '{fullName}', '{address}', {gender}, '{maritalStatus}', {wallet} )
        """)
        mydb.commit()
    except:
        print("ERROR")

#change something about a customer using a dictionary
#That is all the elements in the dictionary of customer with username will be updated
def updateCustomer(username, D):
    for s in D:
        if s == "fullName":
            my_cursor.execute(f"""
                UPDATE customer SET fullName = \"{D[s]}\" WHERE username = \"{username}\";
            """)
            mydb.commit()
        if s == "username":
            my_cursor.execute(f"""
                UPDATE customer SET username = \"{D[s]}\" WHERE username = \"{username}\";
            """)
            mydb.commit()
        if s == "password":
            my_cursor.execute(f"""
                UPDATE customer SET password = \"{D[s]}\" WHERE username = \"{username}\";
            """)
            mydb.commit()

        if s == "address":
            my_cursor.execute(f"""
                UPDATE customer SET Address = \"{D[s]}\" WHERE username = \"{username}\";
            """)
            mydb.commit()        
        if s == "gender":
            my_cursor.execute(f"""
                UPDATE customer SET gender = {D[s]} WHERE username = \"{username}\";
            """)
            mydb.commit()
        if s == "maritalStatus":
            my_cursor.execute(f"""
                UPDATE customer SET maritalStatus = \"{D[s]}\" WHERE username = \"{username}\";
            """)
            mydb.commit()
        if s == "wallet":
            my_cursor.execute(f"""
                UPDATE customer SET wallet = {D[s]} WHERE username = \"{username}\";
            """)
            mydb.commit()


def deleteCustomers():
    my_cursor.execute(f"DROP TABLE customer;")
    mydb.commit()
    my_cursor.execute(f"""
    CREATE TABLE customer(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username varchar(150) UNIQUE,
    password varchar(150) NOT NULL,
    fullName varchar(150) NOT NULL,
    Address varchar(150) NOT NULL,
    Gender Boolean NOT NULL,
    maritalStatus varchar(150) NOT NULL,
    wallet INT NOT NULL
    )
    """)
    mydb.commit()

#You delete the user by his username
def deleteCustomer(username):
    my_cursor.execute(f"DELETE FROM customer WHERE username = \"{username}\"")
    mydb.commit()



#Get the entire DB of customers
def getCustomers():
    my_cursor.execute("Select * FROM customer;") # will return the users as a dictionary
    D = {}
    for(id, username, password, fullName, Address, Gender, maritalStatus, wallet) in my_cursor:
        D[id] = { "username": username, "password": password, "fullName": fullName, "Address": Address, "Gender": Gender, "maritalStatus": maritalStatus, "wallet": wallet }
    return D

#Get a customer by his username
def getCustomer(username):
    my_cursor.execute(f"SELECT * FROM customer WHERE username = \"{username}\"")
    for(id, username, password, fullName, Address, Gender, maritalStatus, wallet) in my_cursor:
        return {"id": id, "username": username, "password": password, "fullName": fullName, "Address": Address, "Gender": Gender, "maritalStatus": maritalStatus, "wallet": wallet }
    return {}

#Give a customer money
def chargeCustomer(username, supply):
    my_cursor.execute(f"Select * FROM customer WHERE username = \"{username}\"")
    for(id, username, password, fullName, Address, Gender, maritalStatus, wallet) in my_cursor:
        wallet_ = wallet + supply
        print(wallet, wallet_, supply)
    my_cursor.execute(f"UPDATE customer SET wallet = {wallet_} WHERE username = \"{username}\"")
    mydb.commit()


#Take money from customer
def deduceCustomer(username, remove):
    my_cursor.execute(f"Select * FROM customer WHERE username = \"{username}\"")
    wallet_ = None
    for(id, username, password, fullName, Address, Gender, maritalStatus, wallet) in my_cursor:
        if(wallet - remove < 0): return False
        else: wallet_ = wallet - remove
        
    my_cursor.execute(f"UPDATE customer SET wallet = {wallet_} WHERE username = \"{username}\"")
    mydb.commit()
    return True
    

