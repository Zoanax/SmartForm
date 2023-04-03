import sqlite3
from tabulate import tabulate



def db_connect():
    # Connect to the database
    db_path = r'./db.sqlite3'
    global conn
    conn = sqlite3.connect(db_path)
    # Create a cursor
    global cursor
    cursor = conn.cursor()


def executeSelect(query):
    cursor.execute(query)
    res = cursor.fetchall()
    printFormat(res)
    return res

def close_connection():
    cursor.close()
    conn.close()

def printFormat(results):
    
    for result in results:
        print(result)


def checkForTask():
    # checks for task to run today and scheduled . 
    print(" # Scheduled Task to Run during this period")
    query =" select task_name, id from smart_emailApp_emailtask Where date_from  BETWEEN date('1004-01-01') AND date('2023-12-31') AND status='Scheduled'; "
    executeSelect(query)

def makeEmail():
    
    pass


db_connect()
# print(executeSelect("SELECT * FROM smart_emailApp_emails"))
checkForTask()