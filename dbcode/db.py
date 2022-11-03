import sqlite3
from dbcode.config import base_db
import os

pre = 'instance/'

def select_migranti():
    connection = sqlite3.connect(pre+base_db)
    cursor = connection.cursor()
    rows = cursor.execute("SELECT nome, cognome, stato FROM migranti").fetchall()
    connection.commit()
    connection.close()
    return rows


def save_file(nome,cognome,file):
    connection = sqlite3.connect(pre + base_db)
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO migranti_files VALUES ('{nome}', '{cognome}', '{file.filename}')")
    dir = 'static/'+nome+'_'+cognome
    os.makedirs(dir,exist_ok=True)
    file.save(dir+'/'+file.filename)
    connection.commit()
    connection.close()

def get_files(nome,cognome):
    connection = sqlite3.connect(pre + base_db)
    cursor = connection.cursor()
    rows = cursor.execute(f"SELECT file FROM migranti_files WHERE nome = '{nome}' AND cognome = '{cognome}'").fetchall()
    connection.commit()
    connection.close()
    return rows