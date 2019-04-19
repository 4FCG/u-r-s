import config
import datetime


def log(uitvoerder, actie):
    file = open(config.log['file'], 'a+')
    file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": '" + uitvoerder + "': " + actie + "\n"))
