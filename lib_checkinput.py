# Is benodigd om te controleren of datums en tijden volgens de juiste wijze zijn geformatteerd.
import datetime

def date(string):
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


def time(string):
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
