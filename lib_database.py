from lib_log import log
from lib_password import hash_password, verify_password

# Probeer om de "mysql.connector"-module te importeren.
try:
    import mysql.connector
except ImportError:
    # Plaats een melding in het logbestand en toon deze in de CLI.
    print(log('MODULES', "[!] Missende module: Python-module 'mysql.connector' is vereist voor dit programma. Installeert u alstublieft de 'mysql.connector'-module met het commando: 'pip install mysql.connector'"))
    exit()

# Probeer om het "config.py"-bestand te importeren.
try:
    import config
except ImportError:
    # Plaats een melding in het logbestand en toon deze in de CLI.
    print(log('CONFIGURATIE', "[!] Configuratiebestand mist: Het configuratie bestand 'config.py' is vereist voor dit programma. Er zal een nieuw configuratie bestand aangemaakt worden."))
    exit()

# Probeer verbinding te maken met de MySQL-database.
try:
    database = mysql.connector.connect(
        host=config.mysql['host'],
        user=config.mysql['user'],
        passwd=config.mysql['passwd'],
        database=config.mysql['database']
    )
except mysql.connector.Error as err:
    # Plaats een melding in het logbestand en toon deze in de CLI.
    log('DATABASE', "[!] Aanmelden bij databaseserver niet gelukt: {}".format(err))
    exit()

cursor = database.cursor()


def add_user(voornaam, achternaam, wachtwoord, functie_id, type_medewerker, mag_thuis, woonafstand, contracturen, uurtarief, manager_id):
    # Voegt een gebruiker toe aan het programma.

    # Bouw de query.
    query = "INSERT INTO `medewerker` (voornaam, achternaam, wachtwoord, functie_id, type_medewerker, mag_thuis, woonafstand, contracturen, uurtarief, manager_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # Stel de parameters samen.
    parameters = (voornaam, achternaam, hash_password(wachtwoord), functie_id, type_medewerker,
                  mag_thuis, woonafstand, contracturen, uurtarief, manager_id)

    # Laat de parameters in de query zetten en voer de query uit.
    cursor.execute(query, parameters)

    # Maak de toevoeging definitief.
    database.commit()

    # Plaats een melding in het logbestand.
    log('GEBRUIKERSREGISTRATIE', "Succesvolle registratie voor: " + voornaam + " " + achternaam)


def login(voornaam, achternaam, wachtwoord):
    cursor.execute(
        "SELECT * FROM MEDEWERKER WHERE voornaam = %s AND achternaam = %s;", (voornaam, achternaam))
    values = list(cursor)
    cursor.execute("SHOW columns FROM MEDEWERKER;")
    columns = list(cursor)
    for row in values:
        if verify_password(row[3], wachtwoord):
            log('LOGIN', "Succesvolle aanmelding voor: " + voornaam + " " + achternaam)
            return {columns[index][0]: value for index, value in enumerate(row)}
    log('LOGIN', "Foutieve aanmelding voor: " + voornaam + " " + achternaam)
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


def wijzigingen_doorvoeren(changelog):
    # Slaat de ingevoerde gegevens op in de database. En werkt de tabel bij.
        live = 1
        for row in changelog:
            tabel = str(row['table']).upper()
            # De primaire sleutel zit altijd in een kolom met als naam de naam van de tabel met daarachter "_id".
            primaire_sleutel = str(tabel.lower() + "_id")
            if row['type'] == 'toevoeging':
                row['data'].pop(primaire_sleutel, None)
            kolommen = list(row['data'].keys())
            waarden = list(row['data'].values())

            if row['type'] == "verwijdering":
                if live == 1:
                    cursor.execute("DELETE FROM " + tabel + " WHERE " + primaire_sleutel + " = " + row['data'][primaire_sleutel] + ";")
                    log('OPSLAAN', "Rij " + row['data'][primaire_sleutel] + " is succesvol verwijderd uit tabel " + tabel)

                    # Speciale uitzondering voor de "DAG" tabel: Wanneer een dag verwijderd word dient ook de activiteiten van deze tabel verwijderd te worden.
                    if tabel == "DAG":
                        cursor.execute("DELETE FROM ACTIVITEITEN WHERE 'werkdag_id' " + " = " + row['data']['dag_id'] + ";")
                        log('OPSLAAN', "[-] Rij " + row['data']['dag_id'] + " is succesvol verwijderd uit tabel ACTIVITEITEN.")
                    database.commit()

                else:
                    print("Verwijderen!")

            elif row['type'] == "toevoeging":
                if live == 1:
                    query = "INSERT INTO " + tabel + " ("
                    for kolom in kolommen:
                        query += "`" + kolom + "`, "
                    query = query[:-2]
                    query += ") VALUES ("
                    for waarde in waarden:
                        query += "'" + waarde + "', "
                    query = query[:-2]
                    query += ");"
                    cursor.execute(query)
                    log('OPSLAAN', "[+] Rij " + str(cursor.lastrowid) + " is succesvol toegevoegd aan tabel " + tabel)
                    database.commit()

                else:
                    print("Toevoegen!")

            elif row['type'] == "verandering":
                if live == 1:
                    query = "UPDATE " + tabel + " SET "

                    huidige_waarde = 0
                    for kolom in kolommen:
                        query += kolom + " = '" + waarden[huidige_waarde] + "', "
                        huidige_waarde += 1
                    query = query[:-2]
                    query += " WHERE " + primaire_sleutel + " = " + row['data'][primaire_sleutel] + ";"
                    cursor.execute(query)
                    log('OPSLAAN', "[|] Rij " + str(cursor.lastrowid) + " is succesvol aangepast in tabel " + tabel)
                    database.commit()
                else:
                    print("Bijwerken!")
