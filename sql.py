import sqlite3
with sqlite3.connect("flaskweb.db") as con:
    c = con.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT NOT NULL, title  TEXT NOT NULL UNIQUE, post TEXT NOT NULL )""")
    c.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, email TEXT NOT NULL UNIQUE)""")
    