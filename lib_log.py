import config
import datetime


def log(uitvoerder, actie):
    file = open(config.log['file'], 'a+')
    melding = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": '" + uitvoerder + "': " + actie + "\n")
    file.write(melding)

    return(melding)
