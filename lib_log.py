import config
import datetime
from os import mkdir


def log(uitvoerder, actie):
    try:
        mkdir(config.log['path'])
    except FileExistsError:
        pass
    with open(config.log['path'] + 'log.txt', 'a+') as file:
        melding = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
                      ": '" + uitvoerder + "': " + actie + "\n")
        file.write(melding)
        return melding
