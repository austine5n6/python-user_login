import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute('''CREATE TABLE users
             (username text, password_hash text)''')

conn.commit()
conn.close()