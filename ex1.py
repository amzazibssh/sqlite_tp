import sqlite3

conn = sqlite3.connect('MyDataBase.db')

c = conn.cursor()


#Exercie 1
c.execute(''' CREATE TABLE client 
            (id INTEGER, Nom TEXT,Rue TEXT,Ville TEXT, Region TEXT, Note REAL)''')

data = [
    (1,'Toto','Rue 1','Lille','Nord',105.2),
    (2,'Bill','Rue 2','Fourmies','Nord',105.2),
    (3,'Ben','Rue 3','Lille','Nord',105.2),
]

c.executemany('INSERT INTO client VALUES (?,?,?,?,?,?)', data)

conn.commit()

c.execute('SELECT * FROM client')
rows = c.fetchall()
for row in rows:
    print(row)

conn.close()