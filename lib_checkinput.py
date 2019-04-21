# Is benodigd om te controleren of datums en tijden volgens de juiste wijze zijn geformatteerd.
import datetime

# Is benodigd om voor het controleren van tekst op basis van illegale tekens.
import re

from lib_database import get_data
from lib_error import error


def check_date(string):
    # Controleert of de opgegeven string een juist geformatteerde datum is.

    # Stel een formaat op met: YYYY-MM-DD, bijvoorbeeld: 2019-04-19
    format = "%Y-%m-%d"
    try:
        # Probeer om de input om te zetten naar een "datetime"-object.
        datetime.datetime.strptime(string, format)

        # Als het lukt return dan "True".
        return True
    except ValueError:
        # Als het niet lukt return dan "False".
        return False


def check_time(string):
    # Controleert of de opgegeven string een juist geformatteerde tijd is.

    # Stel een formaat op met: UU:MM:SS, bijvoorbeeld: 22:24:21
    format = "%H:%M:%S"
    try:
        # Probeer om de input om te zetten naar een "datetime"-object.
        datetime.datetime.strptime(string, format)

        # Als het lukt return dan "True".
        return True
    except ValueError:
        # Als het niet lukt return dan "False".
        return False

def check_illegalcharacters(string):
    # Maak een nieuwe RegEx-object aan die controleerd of dat de "string" alleen karakters bevat die tussen a-z, A-Z, 0-9 of een van de losse karakters ", . ! ? -" is.
    re_compiled = re.compile(r"[a-zA-Z1-9:,.!?-]*")

    # Controleert of de opgegeven string voldoet aan de vereisten van het "re_compiled"-RegEx-object.
    if re_compiled.fullmatch(string):
        # Als het lukt return dan "True"
        return True
    else:
        # Als het lukt return dan "False"
        return False

def check_illegalcharacters_number(string):
    # Maak een nieuwe RegEx-object aan die controleerd of dat de "string" alleen karakters bevat die tussen a-z, A-Z, 0-9 of een van de losse karakters ", . ! ? -" is.
    re_compiled = re.compile(r"[1-9]*")

    # Controleert of de opgegeven string voldoet aan de vereisten van het "re_compiled"-RegEx-object.
    if re_compiled.fullmatch(string):
        # Als het lukt return dan "True"
        return True
    else:
        # Als het lukt return dan "False"
        return False

def is_allowed(date, starttime):
    curtime = datetime.datetime.today()
    weekday = curtime.weekday()

    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    time = datetime.datetime.strptime(starttime, '%H:%M:%S').time()
    dt = datetime.datetime.combine(date, time)

    if weekday > 0:
        last_monday = curtime - datetime.timedelta(days=weekday)
    elif curtime.time() < datetime.time(hour=12, minute=0, second=0, microsecond=0):
        last_monday = curtime - datetime.timedelta(days=7)
    else:
        last_monday = curtime
    last_monday = last_monday.replace(hour=12, minute=0, second=0, microsecond=0)

    return dt > last_monday


def check_input(table, item):
    name = table.horizontalHeaderItem(item.column()).text()
    if name == 'datum':
        if not check_date(item.text()):
            error("Incorrecte invoer", "De datum is niet correct ingevoerd",
                  "Controleert u alstublieft of de datums zijn ingevoerd met dit formaat: JJJJ-MM-DD, bijvoorbeeld: 1998-10-10.")
            item.setText("")
    elif name == 'starttijd' or name == 'eindtijd':
        if not check_time(item.text()):
            error("Incorrecte invoer", "De starttijd is niet correct ingevoerd",
                  "Controleert u alstublieft of de starttijden zijn ingevoerd met dit formaat: U:MM:SS, bijvoorbeeld: 09:22:23.")
            item.setText("")
    elif name == 'thuisofkantoor':
        if item.text() != '0' and item.text() != '1':
            error("Incorrecte invoer", "De 'thuis of kantoor'-keuze is niet correct ingevoerd",
                  "Vult u hier alstublieft een 0 in als u thuis heeft gewerkt en een 1 als u op kantoor heeft gewerkt.")
            item.setText("")

    elif name == 'weekslot':
        if item.text() != '0' and item.text() != '1':
            error("Incorrecte invoer", "De 'weekslot'-keuze is niet correct ingevoerd",
                  "Vult u hier alstublieft een 0 in als u het weekslot wilt uitzetten en een 1 als u het weekslot wilt aanzetten.")
            item.setText("")

    elif name == 'goedgekeurd':
        if item.text() != '0' and item.text() != '1':
            error("Incorrecte invoer", "De 'weekslot'-keuze is niet correct ingevoerd",
                  "Vult u hier alstublieft een 0 in als de activiteit niet goedkeurd en een 1 als u het wel goedkeurd.")
            item.setText("")

    elif name == 'uren':
        if not check_illegalcharacters_number(item.text()):
            error("Incorrecte invoer", "De '" + name + "'-keuze is niet correct ingevoerd",
                  "Vult u hier alstublieft alleen cijfers in.")
            item.setText("")
    #
    # elif name == 'uren':
    #     for rij in get_data("ACTIVITEIT", "activiteiten_id = " + "")
    #
    #
    #
    #     uren_totaal = uren_pw + int(item.text())
    #     if uren_totaal <= 60:
    #         error("Te veel werkuren", "Het maximaal aantal werkuren van deze week is overschreden.",
    #               "Momenteel heeft u ." + "")

    elif name == 'activiteiten_id':
        activiteiten_tekst = ""
        activiteiten_toegestaan = get_data('RECHTEN', 'WHERE functie_id = ' + str(table.user['functie_id']))

        if not int(item.text()) in activiteiten_toegestaan[0].values():
            for rij in get_data("ACTIVITEITEN", ""):
                if rij['activiteiten_id'] in activiteiten_toegestaan[0].values():
                    activiteiten_tekst += "\n- " + str(rij['activiteiten_id']) + ": " + rij['activiteitnaam'] + ": " + \
                                          rij['omschrijving']
            error("Incorrecte invoer", "Deze activiteit bestaat niet",
                  "Plaatst u alstublieft een van de volgende activiteiten:\n " + activiteiten_tekst)
            item.setText("")

    elif not check_illegalcharacters(item.text()):
        error("Incorrecte invoer", "De ingevoerde waarde in de '" + name + "'-kolom is incorrect",
              "Controleert u alstublieft of dat de waarde alleen bestaat uit de volgende tekens: a-z, A-Z, 0-9, ',', '.', '!', '?', ':', '-'.")
    # editing an old date that is now locked will delete it and wont let you put it back
    if (name == 'datum' or name == 'starttijd') and table.tablename == "dag":
        item_row_data = table.get_row_data(item.row())
        if len(item_row_data['datum']) > 0 and len(item_row_data['starttijd']) > 0:
            if not is_allowed(item_row_data['datum'], item_row_data['starttijd']) and table.user['weekslot'] == 1 and table.user['manager_id'] is not None:
                error("Toegang geblokkeerd", "Combinatie datum en starttijd niet toegestaan.",
                      "De combinatie van datum en starttijd die u heeft ingegeven zijn niet toegestaan omdat deze tijd al is afgesloten. Neem contact op met uw manager om deze tijd te openen.")
                item.setText("")
