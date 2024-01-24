import os
import sqlite3
from core.settings import BASE_DIR
import pandas as pd
import sqlite3
from datetime import datetime

tdy = datetime.today().strftime('%Y-%m-%d')
tdy_dtl = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Connecting to the geeks database
connection = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite'),check_same_thread=False)

# Table Definition
def search_log(user, keyword):
    try:
        create_table = '''CREATE TABLE SEARCHLOG (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date DATETIME,
                            keyword TEXT,
                            username TEXT
                            );'''
        cursor = connection.cursor()
        cursor.execute(create_table)
    except:
        pass
    data = pd.DataFrame(list(zip([tdy],[keyword],[user])),
        columns =['date','keyword','username'])
    # insert to DB
    data.to_sql(name='SEARCHLOG', con=connection, if_exists = 'append', index=False)
    countRow = len(data)
    print(f"{countRow} log saved to DB")

def user_log(user, activity):
    try:
        create_table = '''CREATE TABLE ACTLOG (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            datetime DATETIME,
                            activity TEXT,
                            username TEXT
                            );'''
        cursor = connection.cursor()
        cursor.execute(create_table)
    except:
        pass
    data = pd.DataFrame(list(zip([tdy_dtl],[activity],[user])),
        columns =['datetime','activity','username'])
    # insert to DB
    data.to_sql(name='ACTLOG', con=connection, if_exists = 'append', index=False)
    countRow = len(data)
    print(f"{countRow} log saved to DB")
    # connection.close()
