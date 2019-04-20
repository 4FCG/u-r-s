# Is benodigd om te controleren of datums en tijden volgens de juiste wijze zijn geformatteerd.
import datetime
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
    # editing an old date that is now locked will delete it and wont let you put it back
    if (name == 'datum' or name == 'starttijd') and table.tablename == "dag":
        item_row_data = table.get_row_data(item.row())
        if len(item_row_data['datum']) > 0 and len(item_row_data['starttijd']) > 0:
            if not is_allowed(item_row_data['datum'], item_row_data['starttijd']) and table.user['weekslot'] == 1 and table.user['manager_id'] is not None:
                error("Toegang geblokkeerd", "Combinatie datum en starttijd niet toegestaan.",
                      "De combinatie van datum en starttijd die u heeft ingegeven zijn niet toegestaan omdat deze tijd al is afgesloten. Neem contact op met uw manager om deze tijd te openen.")
                item.setText("")
