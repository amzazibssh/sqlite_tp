import sqlite3
from datetime import date

conn = sqlite3.connect('Hotel.sqlite')

c = conn.cursor()
conn.text_factory = lambda b: b.decode(errors = 'ignore')

#fetchall() : récupère toutes les lignes de la requête
client = c.execute('''SELECT * FROM T_CLIENT WHERE CLI_NOM LIKE "%D%"''').fetchall()

#fetchone() : récupère la première ligne de la requête
client = c.execute('''SELECT * FROM T_CLIENT WHERE CLI_NOM LIKE "%D%"''').fetchone()

#fetchmany(n) : récupère les n premières lignes de la requête
client = c.execute('''SELECT * FROM T_CLIENT WHERE CLI_NOM LIKE "%D%"''').fetchmany(5)



def print_info(c):
    while True:
        saisie = input("Numéro de la requête (1 à 8, 0 pour quitter) : ")
        try:
            chiffre = int(saisie)
        except ValueError:
            print("Veuillez saisir un nombre.")
            continue

        if chiffre == 0:
            break

        elif chiffre == 1:
            c.execute("SELECT CLI_NOM, CLI_PRENOM FROM T_CLIENT WHERE TIT_CODE = 'Mme.'")
            for nom, prenom in c.fetchall():
                print(f"Nom: {nom}, Prénom: {prenom}")

        elif chiffre == 2:
            c.execute("SELECT * FROM T_CLIENT WHERE TIT_CODE = 'M.' ORDER BY CLI_NOM")
            for row in c.fetchall():
                print(row)

        elif chiffre == 3:
            c.execute("SELECT CLI_NOM, CLI_PRENOM FROM T_CLIENT WHERE CLI_NOM LIKE 'B%'")
            for nom, prenom in c.fetchall():
                print(f"Nom: {nom}, Prénom: {prenom}")

        elif chiffre == 4:
            c.execute(
                "SELECT DISTINCT FAC_ID FROM T_LIGNE_FACTURE "
                "WHERE (LIF_REMISE_POURCENT IS NULL OR LIF_REMISE_POURCENT = 0) "
                "AND (LIF_REMISE_MONTANT IS NULL OR LIF_REMISE_MONTANT = 0)"
            )
            ids = [str(row[0]) for row in c.fetchall()]
            print("Les identifiants facture (FAC_ID) sans remise sont :", ", ".join(ids))

        elif chiffre == 5:
            aujourdhui = date.today().isoformat()   # ou "2001-01-28" pour tester
            c.execute(
                "SELECT COUNT(*) FROM TJ_CHB_PLN_CLI "
                "WHERE PLN_JOUR = ? AND CHB_PLN_CLI_OCCUPE = 1 AND CHB_PLN_CLI_RESERVE = 0",
                (aujourdhui,)
            )
            print(f"Le nombre de chambres occupées et non réservées le {aujourdhui} est de {c.fetchone()[0]}")

        elif chiffre == 6:
            c.execute("SELECT CHB_ETAGE, COUNT(*) FROM T_CHAMBRE GROUP BY CHB_ETAGE ORDER BY CHB_ETAGE")
            for etage, nb in c.fetchall():
                print(f"L'étage {etage} a {nb} chambres.")

        elif chiffre == 7:
            c.execute("SELECT COUNT(*) FROM T_CHAMBRE WHERE CHB_DOUCHE = 0")
            print(f"Le nombre de chambres sans douche est de {c.fetchone()[0]}")
        elif chiffre == 8:
            try:
                cli_id   = int(input("CLI_ID : "))
                titre    = input("Titre (M., Mme., Mlle.) : ")
                nom      = input("Nom : ")
                prenom   = input("Prénom : ")
                enseigne = input("Enseigne (vide si aucune) : ")

                c.execute(
                    "INSERT INTO T_CLIENT (CLI_ID, TIT_CODE, CLI_NOM, CLI_PRENOM, CLI_ENSEIGNE) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (cli_id, titre, nom, prenom, enseigne or None)
                )
                c.connection.commit()
                print("Client ajouté.")
            except ValueError:
                print("CLI_ID doit être un nombre entier.")
            except sqlite3.Error as e:
                print(f"Erreur lors de l'insertion : {e}")

        else:
            print("Choix invalide.")

print_info(c)

conn.close()