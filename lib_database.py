# Interne python module om logs op te slaan.
from lib_log import log

# Interne python module om wachtwoorde te hashen.
from lib_password import hash_password, verify_password
from os import mkdir, startfile, path

# Interne python module om foutmeldingen te tonen.
from lib_error import error

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
    print(log('CONFIGURATIE',
              "[!] Configuratiebestand mist: Het configuratie bestand 'config.py' is vereist voor dit programma. Er zal een nieuw configuratie bestand aangemaakt worden."))
    exit()

# Probeer verbinding te maken met de MySQL-database. Met behulp van de instellingen uit "config.py".
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
    # Controleerd of de inloggegevens correct zijn.

    # Voer een query uit om uit te zoeken of de opgegeven voornaam en achternaam bestaan in de database.
    cursor.execute(
        "SELECT * FROM MEDEWERKER WHERE voornaam = %s AND achternaam = %s;", (voornaam, achternaam))

    # Sla de resultaten op in "values".
    values = list(cursor)

    # Haal de kolommen op uit tabel MEDEWERKER.
    cursor.execute("SHOW columns FROM MEDEWERKER;")

    # S;a de resultaten van de vorige query op in ""columns".
    columns = list(cursor)

    # Voor iedere rij in "values".
    for row in values:
        # Controleer of de hash van het ingevoerde wachtwoord overeenkomt met de hash in de database van een van de gebruikers.
        if verify_password(row[3], wachtwoord):
            # Indien het lukt sla in het log op dat het gelukt is.
            log('LOGIN', "Succesvolle aanmelding voor: " + voornaam + " " + achternaam)

            # Geef de informatie van de ingelogde gebruiker door.
            return {columns[index][0]: value for index, value in enumerate(row)}

    # Sla op in het log dat het inloggen is mislukt.
    log('LOGIN', "Foutieve aanmelding voor: " + voornaam + " " + achternaam)

    # Indien er geen resultaten gevonden zijn return False.
    return False


def get_data(tablename, specifier):
    # Verkrijg gemakkelijk data uit de database.

    # Voer een SELECT-query uit op "tablename" met als verdere argumenten "specifier".
    cursor.execute("SELECT * FROM " + tablename + " " +
                   ("" if specifier is None else specifier) + ";")

    # Sla de opgehaalde gegevens op in "values".
    values = list(cursor)

    # Verkrijg alle kolommen uit de table.
    cursor.execute("SHOW columns FROM " + tablename + ";")

    # Sla de verkregen kolommen op in "columns".
    columns = list(cursor)

    # Maak een nieuwe list aan genaamd "data".
    data = []

    # Voor iedere rij in "values".
    for row in values:

        # Voeg een nieuwe rij toe in "data" met de waardes uit "values".
        data.append({column[0]: row[index] for index, column in enumerate(columns)})

    # Geef terug "data".
    return data


def wijzigingen_doorvoeren(changelog):
    # Deze functie wordt pas uitgevoerd wanneer de gebruiker op "Opslaan" klikt.
    # Slaat de ingevoerde gegevens op in de database. En werkt de tabel bij.
    if changelog != []:
        live = 1
        # Voor iedere "row" (iedere keer wanneer de visuele tabel wordt aangepast wordt  de verandering opgeslagen in "changelog").
        for row in changelog:
            tabel = str(row['table']).upper()
            # De primaire sleutel zit altijd in een kolom met als naam de naam van de tabel met daarachter "_id".
            primaire_sleutel = str(tabel.lower() + "_id")
            if row['type'] == 'toevoeging':
                row['data'].pop(primaire_sleutel, None)
            kolommen = list(row['data'].keys())
            waarden = list(row['data'].values())

            if row['type'] == "verwijdering":
                # Is handig voor het testen. Zo kunnen we de interne programmatuur van het programma testen zonder perongeluk onze database aan te passen.
                if live == 1:
                    cursor.execute("DELETE FROM " + tabel + " WHERE " +
                                   primaire_sleutel + " = " + row['data'][primaire_sleutel] + ";")
                    log('OPSLAAN', "Rij " + row['data'][primaire_sleutel] +
                        " is succesvol verwijderd uit tabel " + tabel)

                    # Speciale uitzondering voor de "DAG" tabel: Wanneer een dag verwijderd word dient ook de activiteiten van deze tabel verwijderd te worden.
                    if tabel == "DAG":
                        cursor.execute("DELETE FROM ACTIVITEITEN WHERE 'werkdag_id' " +
                                       " = " + row['data']['dag_id'] + ";")
                        log('OPSLAAN', "[-] Rij " + row['data']['dag_id'] +
                            " is succesvol verwijderd uit tabel ACTIVITEITEN.")
                    database.commit()

                else:
                    print("Verwijderen!")

            elif row['type'] == "toevoeging":
                # Is handig voor het testen. Zo kunnen we de interne programmatuur van het programma testen zonder perongeluk onze database aan te passen.
                if live == 1:

                    # De volgende code bouwt een INSTERT-INTO-query, de onderstaande regelscode doen niks meer dan het normaliseren van de query.
                    # Het zorgt ongeacht de grootte, het aantal rijen en waarden altijd een juiste INSERT-INTO-query.
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
                    log('OPSLAAN', "[+] Rij " + str(cursor.lastrowid) +
                        " is succesvol toegevoegd aan tabel " + tabel)
                    database.commit()

                else:
                    print("Toevoegen!")

            elif row['type'] == "verandering":
                # Is handig voor het testen. Zo kunnen we de interne programmatuur van het programma testen zonder perongeluk onze database aan te passen.
                if live == 1:

                    # De volgende code bouwt een UPDATE-query, de onderstaande regelscode doen niks meer dan het normaliseren van de query.
                    # Het zorgt ongeacht de grootte, het aantal rijen en waarden altijd een juiste UPDATE-query.
                    query = "UPDATE " + tabel + " SET "

                    huidige_waarde = 0
                    for kolom in kolommen:
                        query += kolom + " = '" + waarden[huidige_waarde] + "', "
                        huidige_waarde += 1
                    query = query[:-2]
                    query += " WHERE " + primaire_sleutel + \
                        " = " + row['data'][primaire_sleutel] + ";"
                    cursor.execute(query)
                    log('OPSLAAN', "[|] Rij " + str(cursor.lastrowid) +
                        " is succesvol aangepast in tabel " + tabel)
                    database.commit()
                else:
                    print("Bijwerken!")

        changelog.clear()


def csv(rapport, tabellen):
    try:
        # Probeer een folder aan te maken voor de rapporten.
        mkdir('rapporten')
    except FileExistsError:
        # Indien de folder al bestaat ga verder.
        pass
    try:
        # Probeer een bestand aan te maken voor het rapport.
        mkdir('rapporten/' + rapport)
    except FileExistsError:
        # Indien deze al bestaat ga verder.
        pass

    # Voor iedere key in de dictionary "tabellen".
    for tabel in list(tabellen.keys()):
        columns = tabellen[tabel]
        query = "SELECT " + ', '.join(columns) + ' FROM ' + tabel + ";"
        cursor.execute(query)
        rows = list(cursor)
        with open('rapporten/' + rapport + '/' + tabel + '.txt', 'w') as file:
            file.write(';'.join(['"' + column + '"' for column in columns]) + '\n')
            for row in rows:
                file.write(';'.join(['"' + value + '"' if isinstance(value, str)
                                     else str(value) for value in row]) + '\n')
    try:
        startfile(path.realpath('rapporten/' + rapport))
    except:
        error("Rapport gegenereerd", 'Het gevraagde rapport is te vinden in:', 'rapporten/' + rapport)
