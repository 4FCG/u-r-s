import mysql.connector
import config
from lib_password import hash_password, verify_password

database = mysql.connector.connect(
    host=config.mysql['host'],
    user=config.mysql['user'],
    passwd=config.mysql['passwd'],
    database=config.mysql['database']
)

cursor = database.cursor()


def add_user(voornaam, achternaam, wachtwoord, functie_id, type_medewerker, mag_thuis, woonafstand, contracturen, uurtarief, manager_id):
    query = "INSERT INTO `medewerker` (voornaam, achternaam, wachtwoord, functie_id, type_medewerker, mag_thuis, woonafstand, contracturen, uurtarief, manager_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    parameters = (voornaam, achternaam, hash_password(wachtwoord), functie_id, type_medewerker,
                  mag_thuis, woonafstand, contracturen, uurtarief, manager_id)
    cursor.execute(query, parameters)
    database.commit()


def login(voornaam, achternaam, wachtwoord):
    cursor.execute(
        "SELECT * FROM MEDEWERKER WHERE voornaam = %s AND achternaam = %s;", (voornaam, achternaam))
    values = list(cursor)
    cursor.execute("SHOW columns FROM MEDEWERKER;")
    columns = list(cursor)
    for row in values:
        if verify_password(row[3], wachtwoord):
            return {columns[index][0]: value for index, value in enumerate(row)}
    return False


def get_data(tablename, specifier):
    cursor.execute("SELECT * FROM " + tablename + " " +
                   ("" if specifier is None else specifier) + ";")
    values = list(cursor)
    cursor.execute("SHOW columns FROM " + tablename + ";")
    columns = list(cursor)
    data = []
    for row in values:
        data.append({column[0]: row[index] for index, column in enumerate(columns)})
    return data
#add_user('John', 'Depper', 'TheJohn', 2, 1, 1, 40.5, 36, 16.50, None)


def wijzigingen_doorvoeren(changelog):
    # Slaat de ingevoerde gegevens op in de database. En werkt de tabel bij.
        live = 1
        for row in changelog:
            tabel = row['table']
            # De primaire sleutel zit altijd in een kolom met als naam de naam van de tabel met daarachter "_id".
            primaire_sleutel = str(tabel.lower() + "_id")
            if row['type'] == 'toevoeging':
                row['data'].pop(primaire_sleutel, None)
            kolommen = list(row['data'].keys())
            waarden = list(row['data'].values())

            if row['type'] == "verwijdering":
                if live == 1:
                    query_variabelen = []
                    query_variabelen += tabel, primaire_sleutel, row['data'][primaire_sleutel]
                    cursor.execute("DELETE FROM %s WHERE `%s` = %s;", query_variabelen)

                    # Speciale uitzondering voor de "DAG" tabel: Wanneer een dag verwijderd word dient ook de activiteiten van deze tabel verwijderd te worden.
                    if tabel == "DAG":
                        query_variabelen = []
                        query_variabelen += "ACTIVITEIT", "werkdag_id", row['data']['dag_id']
                        cursor.execute("DELETE FROM %s WHERE `%s` = %s;", query_variabelen)

                else:
                    print("Verwijderen!")

            elif row['type'] == "toevoeging":
                if live == 1:
                    query_pre = "INSERT INTO `%s` ("
                    query_middel = ") VALUES ("
                    query_post = ")"
                    for kolom in kolommen:
                        query_pre += "`%s`, "

                    for waarde in waarden:
                        query_middel += "%s, "

                    query_waarden = [tabel]
                    for kolom in kolommen:
                        query_waarden.append(kolom)
                    for waarde in waarden:
                        query_waarden.append(waarde)

                    query = query_pre[:-2] + query_middel[:-2] + query_post
                    print("Bijwerking, Query:" + query)
                    print("Bijwerking, Query waarden:" + str(query_waarden))

                    cursor.execute(query, query_waarden)

                else:
                    print("Toevoegen!")

            elif row['type'] == "verandering":
                if live == 1:
                    query_pre = "UPDATE %s ("
                    query_middel = ") VALUES ("
                    query_post = ")"
                    for kolom in kolommen:
                        query_pre += "`%s`, "

                    for waarde in waarden:
                        query_middel += "%s, "

                    query_waarden = [tabel]
                    for kolom in kolommen:
                        query_waarden.append(kolom)
                    for waarde in waarden:
                        query_waarden.append(waarde)

                    query = query_pre[:-2] + query_middel[:-2] + query_post
                    print("Verandering, Query: " + query)
                    print("Verandering, Query waarden: " + str(query_waarden))

                    cursor.execute(query, query_waarden)
                else:
                    print("Bijwerken!")
