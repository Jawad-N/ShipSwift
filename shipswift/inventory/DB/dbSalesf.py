import mysql.connector 


mydb = mysql.connector.connect(
    host = "172.17.0.1",
    user = "root",
    passwd = "12345",
    port = 3307
)


mydb.reset_session()
my_cursor = mydb.cursor()
  
my_cursor.execute(" USE DB ")
mydb.commit()

##################################################### functions that control customer db

def addPurchase(user, item, count, price): #Note that date is a timestamp so when entered to the table it automatically calls NOW() in mysql to record the current time
    my_cursor.execute(f"""
    INSERT INTO log(buyer, item, count, price)     
        VALUES('{user}', '{item}', {count}, {price})        
""")
    mydb.commit()


def listItems():
    try:
        my_cursor.execute(f"""
            SELECT * FROM inventory;
        """)
        D = {}
        for(id, name, category, price, description, count) in my_cursor:
            D[name] = { "price": price }
        return D
    except:
        return False

    
def listItem(name):
    try:
        my_cursor.execute(f"""
            SELECT * FROM inventory WHERE name = \"{name}\"
        """)
        D = {}
        for(id, name, category, price, description, count) in my_cursor:
            D[name] = {
                      "category": category,
                      "price": price,
                      "description": description,
                      "count": count  
                    }
        return D
    except:
        return False


def user_log(user):
    my_cursor.execute(f"""
        SELECT * FROM log WHERE buyer = \"{user}\"
    """)
    D = {}
    ctr = 0
    for(id, buyer, item, count, price, date) in my_cursor:
        print( (id, buyer, item, count, price, date), count )
        D[ctr] = (buyer, item, count, price, str(date))
        ctr = ctr + 1
    print(D)
    return D
    
