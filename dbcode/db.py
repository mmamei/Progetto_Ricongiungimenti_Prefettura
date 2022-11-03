import sqlite3
from dbcode.config import base_db

pre = 'instance/'

def select_migranti():
    connection = sqlite3.connect(pre+base_db)
    cursor = connection.cursor()
    rows = cursor.execute("SELECT nome, cognome, stato FROM migranti").fetchall()
    connection.commit()
    connection.close()
    return rows