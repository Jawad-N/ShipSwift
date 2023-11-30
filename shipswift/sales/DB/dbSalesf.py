import mysql.connector 


mydb = mysql.connector.connect(
    host = "172.17.0.1",
    user = "root",
    passwd = "12345",
    port = 3307
)


mydb.reset_session()
my_cursor = mydb.cursor()
  
##################################################### functions that control customer db

def addPurchase(user, item, count, price, date): #Note that date is a timestamp so when entered to the table it automatically calls NOW() in mysql to record the current time
    my_cursor.execute(f"""
    INSERT INTO log(buyer, item, count, price)     
        VALUES('{user}', '{item}', {count}, {price})        
""")
