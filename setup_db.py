import sqlite3

connection = sqlite3.connect("packages.db")

cursor = connection.cursor()
cursor.execute("ALTER TABLE packages RENAME COLUMN box_type TO package_type")
connection.commit()