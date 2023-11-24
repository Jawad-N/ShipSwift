import mysql.connector 


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "12345",
)


mydb.reset_session()
my_cursor = mydb.cursor()

##################################################### functions that control customer db

def addPurchase(user, item, count, price, date):
    my_cursor.execute(f"""
    INSERT INTO log(buyer, item, count, price, date)    
        VALUES('{user}', '{item}', {count}, {price}, {date})  
                    
""")
