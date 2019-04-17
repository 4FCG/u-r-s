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


def rij_verwijder(tabel, kolom, waarde):
    cursor.execute(str("DELETE FROM " + str(tabel) + " WHERE `" + str(kolom) + "` = '" + str(waarde) + "';"))


def rij_toevoegen(tabel, kolommen, waarden):
    kolommen_str = str(kolommen).replace("\'", "`")
    cursor.execute(str("INSERT INTO " + (tabel) + " " + str(kolommen_str) + " VALUES " + str(waarden) + ";"))

def rij_bijwerken(tabel, kolommen, waarden):
    kolommen_str = str(kolommen).replace("\'", "`")
    cursor.execute(str("UPDATE " + str(tabel) + " " + str(kolommen_str) + " VALUES " + str(waarden) + ";"))

