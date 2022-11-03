import sqlite3
from config import base_db

prefix = '../instance/'

if __name__ == '__main__':
    connection = sqlite3.connect(prefix+base_db)
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS migranti (nome TEXT, cognome TEXT, stato INTEGER, PRIMARY KEY (nome, cognome))")
    connection.commit()
    connection.close()

    connection = sqlite3.connect(prefix + base_db)
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS migranti_files (nome TEXT, cognome TEXT, file TEXT, PRIMARY KEY (nome, cognome,file))")
    connection.commit()
    connection.close()

    connection = sqlite3.connect(prefix+base_db)
    cursor = connection.cursor()
    with open('init_data.csv') as f:
        for l in f:
            nome,cognome,n = l.strip().split(',')
            cursor.execute(f"INSERT INTO migranti VALUES ('{nome}', '{cognome}', {int(n)})")

    connection.commit()
    connection.close()

    print('Finished')


