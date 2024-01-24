import os
import glob
import pandas as pd

# import csv
import sqlite3
 
# Connecting to the geeks database
connection = sqlite3.connect('db.sqlite')
 
# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

# Table Definition
try:
    # create_table1 = '''CREATE TABLE SENGKETA (
    #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                     file_names TEXT,
    #                     pokok_sengketa TEXT,
    #                     putusan TEXT,
    #                     );'''
    # create_table2 = '''CREATE TABLE HASIL (
    #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                     file_names TEXT,
    #                     putusan TEXT,
    #                     );'''
    
    create_table3 = '''CREATE TABLE SAMPEL (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_names TEXT,
                        pokok_sengketa TEXT,
                        hasil_putusan TEXT,
                        );'''
    
    # cursor.execute(create_table1)
    # cursor.execute(create_table2)
    cursor.execute(create_table3)
except:
    pass

# df = pd.read_feather('textSengketa.feather')
# df.to_sql(name='SENGKETA', con=connection, if_exists = 'append', index=False)
# countRow = len(df)
# print(f"finished adding {countRow} to DB SENGKETA")
 
# df = pd.read_feather('textPutusan.feather')
# df.to_sql(name='HASIL', con=connection, if_exists = 'append', index=False)
# countRow = len(df)
# print(f"finished adding {countRow} to DB HASIL")

df = pd.read_feather('media/gvsample.ft')
df = df[['file_names','pokok_sengketa','hasil_putusan']]
df.to_sql(name='SAMPEL', con=connection, if_exists = 'append', index=False)
countRow = len(df)
print(f"finished adding {countRow} to DB SAMPEL")

connection.commit()
connection.close()