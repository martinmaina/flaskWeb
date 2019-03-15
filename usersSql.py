

import sqlite3

with sqlite3.connect("flaskwebUsers.db") as con:
    c = con.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL)""")