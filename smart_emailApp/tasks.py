import sqlite3
from tabulate import tabulate




def db_connect():
    # Connect to the database
    db_path = r'C:\Users\giova\OneDrive\Bureau\Program File\SmartForm\db.sqlite3'
    global conn
    conn = sqlite3.connect(db_path)
    # Create a cursor
    global cursor
    cursor = conn.cursor()



def executeSelect(query):
    cursor.execute(query)
    res = printFormat(cursor.fetchall())
    return res

def close_connection():
    cursor.close()
    conn.close()




def printFormat(results):
    
    for result in results:
        print(result)

db_connect()
print(executeSelect("SELECT * FROM smart_emailApp_emails"))
