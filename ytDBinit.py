#Z Akerele

import sqlite3 as s3 

#db name
conn = s3.connect('youtubeshuffler.db')


c = conn.cursor()

#create table
try:
    c.execute('''CREATE TABLE videos
             (URL text primary key, title text, creator text, game text )''')
except:
    print("Error creating table; does it already exist?")