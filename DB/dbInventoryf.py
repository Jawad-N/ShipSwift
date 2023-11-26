import mysql.connector 


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "12345",
)


mydb.reset_session()
my_cursor = mydb.cursor()



##################### Functions that control the db of the inventory

def add(name, category, price, description, count):
    my_cursor.execute(f"""INSERT INTO items( name, category, price, description, count )  
                      VALUES( '{name}', '{category}', {price}, '{description}', {count} )
    """)
    mydb.commit()

def retrieve(name):
    my_cursor.execute(f"""
        SELECT * FROM items WHERE name = {name}
    """)

def deduce(name, val):
    my_cursor.execute(f"""
        Update items SET count = {val} name = {name}
    """)

def updateItem(name, D):
    for s in D:
        if s == "name":
            my_cursor.execute(f"""
                UPDATE items SET name = {D[s]} WHERE username = {name};
            """)
        if s == "category":
            my_cursor.execute(f"""
                UPDATE items SET category = {D[s]} WHERE username = {name};
            """)
        if s == "price":
            my_cursor.execute(f"""
                UPDATE items SET price = {D[s]} WHERE username = {name};
            """)
        if s == "gender":
            my_cursor.execute(f"""
                UPDATE items SET description = {D[s]} WHERE username = {name};
            """)
        if s == "maritalStatus":
            my_cursor.execute(f"""
                UPDATE items SET count = {D[s]} WHERE username = {name};
            """)
        mydb.commit()