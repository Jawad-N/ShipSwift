import mysql.connector 


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "12345",
)


mydb.reset_session()
my_cursor = mydb.cursor()

##################################################### functions that control customer db


def registerCustomer(username, password, fullName, address, gender, maritalStatus):
    my_cursor.execute(f"""INSERT INTO customer(username, password,fullName, Address, Gender, maritalStatus)  
                      VALUES( '{username}', '{password}',  '{fullName}', '{address}', {gender}, '{maritalStatus}')
    """)
    mydb.commit()
    


def getCustomers():
    my_cursor.execute("Select * FROM customer;") # will return the users as a dictionary
    D = {}
    for(id, username, password, fullName, Address, Gender, maritalStatus) in my_cursor:
        D[id] = { "username": username, "password": password, "fullName": fullName, "Address": Address, "Gender": Gender, "maritalStatus": maritalStatus }
    return D


#You delete the user by his username
def deleteCustomer(username):
    my_cursor.execute(f"DELETE FROM customer WHERE username = {username};")
    mydb.commit()
    


