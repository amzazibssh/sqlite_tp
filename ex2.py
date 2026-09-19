import sqlite3

conn = sqlite3.connect('MyDataBase.db')

c = conn.cursor()

c.execute("PRAGMA foreign_keys = ON")

#Exercie 2
def create_tables(c):
    c.execute(''' CREATE TABLE country
                (name Text primary key, gdp REAL)''')

    c.execute(''' CREATE TABLE region(
                    country Text , 
                    name Text ,
                    population Integer,
                    area Integer,
                    primary key(country, name),
                    foreign key(country) references country(name)
                    )''')

    c.execute(''' CREATE TABLE log(
                    id Integer primary key,
                    country Text not null,
                    region Text not null,
                    date Text not null,
                    temperature REAL not null,
                    humidity REAL not null,
                    Unique(country, region, date),
                    foreign key(country, region) references region(country, name)
                    )''')

def insert_data(c):
    c.execute(
        "INSERT INTO country VALUES (?, ?)",
        ("France", 38128)
    )

    c.execute(
        "INSERT INTO country VALUES (?, ?)",
        ("Norway", 70392)
    )

    c.execute(
        "INSERT INTO country VALUES (?, ?)",
        ("Spain", 26609)
    )


    c.execute(
        "INSERT INTO region VALUES (?, ?, ?, ?)",
        ("France", "Hauts-de-France", 5973098, 31813)
    )

    c.execute(
        "INSERT INTO region VALUES (?, ?, ?, ?)",
        ("France", "Île-de-France", 12005077, 12012)
    )

    c.execute(
        "INSERT INTO region VALUES (?, ?, ?, ?)",
        ("France", "Normandie", 3322757, 29906)
    )


    c.execute(
        "INSERT INTO log VALUES (?, ?, ?, ?, ?, ?)",
        (1, "France", "Hauts-de-France", "2017-05-23", 21.1, 51.4)
    )

    c.execute(
        "INSERT INTO log VALUES (?, ?, ?, ?, ?, ?)",
        (2, "France", "Hauts-de-France", "2017-05-24", 23.1, 62.4)
    )

    c.execute(
        "INSERT INTO log VALUES (?, ?, ?, ?, ?, ?)",
        (3, "France", "Hauts-de-France", "2017-05-25", 17.5, 71.1)
    )

conn.commit()


def get_country_starting_with_fr(c):
    c.execute(
        'SELECT * FROM country WHERE name LIKE "FR%"'
    )
    return c.fetchall()


def drop_country(c):
    while True:
        country_name = input("Enter the name of the country to delete: ")
        try:
            c.execute(
                "DELETE FROM country WHERE name = ?",
                (country_name,)
            )
            conn.commit()
            print(f"Country '{country_name}' deleted successfully.")
            break
        except sqlite3.IntegrityError:
            print(f"Cannot delete country '{country_name}' because it is referenced in the region table. Please delete the corresponding regions first.")


all_country = get_country_starting_with_fr(c)

if all_country:
    print("yes")
else:
    print("no") 

drop_country(c)