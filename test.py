import sqlite3

connection = sqlite3.connect("aquarium.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS fish (name TEXT PRIMARY KEY NOT NULL, species TEXT, tank_number INTEGER)")
connection.commit()
connection.close()

connection = sqlite3.connect("aquarium.db")
cursor = connection.cursor()
cursor.execute("INSERT INTO fish VALUES ('Marco', 'shark', 1)")
cursor.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")
connection.commit()
connection.close()

connection = sqlite3.connect("aquarium.db")
cursor = connection.cursor()
rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)
connection.commit()
connection.close()