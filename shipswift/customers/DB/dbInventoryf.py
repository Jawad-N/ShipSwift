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


##################### Functions that control the db of the inventory


def add(name, category, price, description, count):
    my_cursor.execute(f"SELECT * FROM inventory WHERE name = \"{name}\"")
    b = True
    for(id, name, category, price, description, count) in my_cursor:
        b = False
    if(not b): return 0
    try:
        my_cursor.execute(f"""INSERT INTO inventory(name, category, price, description, count)  
                        VALUES( '{name}', '{category}',  {price}, '{description}', {count} )
        """)
        mydb.commit()
        return 1
    except:
       return 2
    
def display():
    try:
        my_cursor.execute(f"""
            SELECT * FROM inventory;
        """)
        D = {}
        for(id, name, category, price, description, count) in my_cursor:
            D[id] = { "name": name,
                      "category": category,
                      "price": price,
                      "description": description,
                      "count": count  
                    }
        return D
    except:
        return False
    
def retrieve(name):
    try:
        my_cursor.execute(f"""
            SELECT * FROM inventory WHERE name = \"{name}\"
        """)
        D = {}
        for(id, name, category, price, description, count) in my_cursor:
            D[id] = { "name": name,
                      "category": category,
                      "price": price,
                      "description": description,
                      "count": count  
                    }
        return D
    except:
        return False
    
def deduce(name):
    my_cursor.execute(f"""
        SELECT * FROM inventory WHERE name = \"{name}\"
    """)
    val = -2
    for(id, _name, category, price, description, count) in my_cursor:
        if(_name == name):
            val = count - 1
    if (val == -2): return 0
    elif (val == -1): return 1 
    else:
        try:
            my_cursor.execute(f"""
                Update inventory SET count = {val} WHERE name = \"{name}\"
            """)
            mydb.commit()
            return 2
        except Exception as e:
            return 3

def deduce2(name,val):
    my_cursor.execute(f"""
        SELECT * FROM inventory WHERE name = \"{name}\"
    """)
    curr = None
    val = int(val)
    for(id, _name, category, price, description, count) in my_cursor:
        if(_name == name):
            curr = count 
    if (curr == None): return 0
    elif (curr - val < 0): return 1 
    else:
        try:
            my_cursor.execute(f"""
                Update inventory SET count = {curr - val} WHERE name = \"{name}\"
            """)
            mydb.commit()
            return 2
        except Exception as e:
            return 3

def updateItem(name, D):
    print(name)
    s = f"SELECT * FROM inventory WHERE name = \"{name}\""
    print(s)
    my_cursor.execute(s)
    b = False
    for(id, _name, category, price, description, count) in my_cursor:
        b = True
    if not b: return 0 # to say there is no elements that have the name for which we are updating
    try:
        if "category" in D:
            my_cursor.execute(f"""
                UPDATE inventory SET category = \"{D["category"]}\" WHERE name = \"{name}\";
            """)
            mydb.commit()
        if "price" in D:
            my_cursor.execute(f"""
                UPDATE inventory SET price = {D["price"]} WHERE name = \"{name}\";
            """)
            mydb.commit()
        if "description" in D:
            my_cursor.execute(f"""
                UPDATE inventory SET description = \"{D["description"]}\" WHERE name = \"{name}\";
            """)
            mydb.commit()

        if "name" in D:
            my_cursor.execute(f"""
                UPDATE inventory SET name = \"{D["name"]}\" WHERE name = \"{name}\";
            """)
            mydb.commit()
   
        return 1 # successful update
    except Exception as e:
        print(e)
        if(type(e) == mysql.connector.errors.IntegrityError): return 2
        return 3 # to indicate unsuccesful update, due to DB errors
    
            