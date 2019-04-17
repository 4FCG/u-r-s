import mysql.connector
import config
from pbkdf2 import hash_password, verify_password

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
        "SELECT medewerker_id, voornaam, wachtwoord FROM MEDEWERKER WHERE voornaam = %s AND achternaam = %s;", (voornaam, achternaam))
    for result in list(cursor):
        if verify_password(result[2], wachtwoord):
            return {'id': result[0], 'naam': result[1]}
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
