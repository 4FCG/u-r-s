def log(bestand, datum, tijdstip, uitvoerder, actie):
    bestand.write(str(datum + ": " + tijdstip + ": '" + uitvoerder + "': " + actie + "\n"))
