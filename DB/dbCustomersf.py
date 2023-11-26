import mysql.connector 


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "12345",
)


mydb.reset_session()
my_cursor = mydb.cursor()

##################################################### functions that control customer db

def registerCustomer(username, password, fullName, address, gender, maritalStatus, wallet):
    my_cursor.execute(f"""INSERT INTO customer(username, password,fullName, Address, Gender, maritalStatus)  
                      VALUES( '{username}', '{password}',  '{fullName}', '{address}', {gender}, '{maritalStatus}', {wallet} )
    """)
    mydb.commit()
    


def updateCustomer(username, D): # you pass in the fields you want to update in a dictionary

    for s in D:
        if s == "username":
            my_cursor.execute(f"""
                UPDATE customer SET username = {D[s]} WHERE username = {username};
            """)
        if s == "password":
            my_cursor.execute(f"""
                UPDATE customer SET password = {D[s]} WHERE username = {username};
            """)
        if s == "Address":
            my_cursor.execute(f"""
                UPDATE customer SET Address = {D[s]} WHERE username = {username};
            """)
        if s == "gender":
            my_cursor.execute(f"""
                UPDATE customer SET gender = {D[s]} WHERE username = {username};
            """)
        if s == "maritalStatus":
            my_cursor.execute(f"""
                UPDATE customer SET maritalStatus = {D[s]} WHERE username = {username};
            """)
        if s == "wallet":
            my_cursor.execute(f"""
                UPDATE customer SET wallet = {D[s]} WHERE username = {username};
            """)
        mydb.commit()



#You delete the user by his username
def deleteCustomer(username):
    my_cursor.execute(f"DELETE FROM customer WHERE username = {username};")
    mydb.commit()

def getCustomers():
    my_cursor.execute("Select * FROM customer;") # will return the users as a dictionary
    mydb.commit()
    D = {}
    for(id, username, password, fullName, Address, Gender, maritalStatus, wallet) in my_cursor:
        D[id] = { "username": username, "password": password, "fullName": fullName, "Address": Address, "Gender": Gender, "maritalStatus": maritalStatus, "wallet": wallet }
    return D

def getCustomer(username):
    my_cursor.execute(f"SELECT * FROM customer WHERE username = {username}")
    mydb.commit()
    for(id, username, password, fullName, Address, Gender, maritalStatus, wallet) in my_cursor:
        return {"id": id, "username": username, "password": password, "fullName": fullName, "Address": Address, "Gender": Gender, "maritalStatus": maritalStatus, "wallet": wallet }
    

def chargeCustomer(username, supply):
    my_cursor.execute(f"Select * FROM customer WHERE username = {username}")
    mydb.commit()
    wallet_ = None
    for(id, username, password, fullName, Address, Gender, maritalStatus, wallet) in my_cursor:
        wallet_ = wallet
    my_cursor.execute(f"UPDATE customer SET wallet = {wallet_ + supply} WHERE username = {username}")
    mydb.commit()

def deduceCustomer(username, remove):
    my_cursor.execute(f"Select * FROM customer WHERE username = {username}")
    mydb.commit()
    wallet_ = None
    for(id, username, password, fullName, Address, Gender, maritalStatus, wallet) in my_cursor:
        wallet_ = wallet
    my_cursor.execute(f"UPDATE customer SET wallet = {wallet_ - remove} WHERE username = {username}")
    mydb.commit()
    


