import sqlite3

connection = sqlite3.connect("packages.db")

cursor = connection.cursor()
cursor.execute("""
CREATE TABLE packages(
    id INTEGER PRIMARY KEY,
    tracking_number TEXT, 
    recipient_name TEXT, 
    date_logged TEXT, 
    date_picked_up TEXT, 
    status TEXT
    )
""")
connection.commit()