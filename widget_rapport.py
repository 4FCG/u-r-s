from lib_database import csv
from PyQt5 import QtWidgets, QtCore


class Rapport_buttons(QtWidgets.QButtonGroup):
    def __init__(self, tab):
        super().__init__(tab)
        self.setExclusive(True)

        self.rapporten = {
            'maandoverzicht': {
                'ACTIVITEITEN': ['activiteiten_id', 'activiteitnaam'],
                'MEDEWERKER': ['medewerker_id', 'uurtarief', 'voornaam', 'achternaam'],
                'DAG': ['thuisofkantoor', 'dag_id', 'goedgekeurd', 'medewerker_id'],
                'ACTIVITEIT': ['uren', 'werkdag_id', 'activiteiten_id']
            },
            'thuiswerktijd': {
                'MEDEWERKER': ['medewerker_id'],
                'DAG': ['thuisofkantoor', 'dag_id', 'goedgekeurd', 'medewerker_id'],
                'ACTIVITEIT': ['uren', 'werkdag_id']
            },
            'woon-werkverkeer': {
                'MEDEWERKER': ['medewerker_id', 'woonafstand'],
                'DAG': ['thuisofkantoor', 'datum', 'goedgekeurd', 'medewerker_id']
            },
            'bezettingsgraad': {
                'MEDEWERKER': ['medewerker_id', 'contracturen', 'voornaam', 'achternaam'],
                'DAG': ['dag_id', 'goedgekeurd', 'medewerker_id'],
                'ACTIVITEIT': ['uren', 'werkdag_id']
            },
            'beschikbaarheid': {
                'DAG': ['dag_id', 'goedgekeurd'],
                'ACTIVITEIT': ['uren', 'werkdag_id']
            }
        }

        for index, rapport in enumerate(list(self.rapporten.keys())):
            button = QtWidgets.QPushButton(tab)
            button.setGeometry(QtCore.QRect(10 + (110 * index), 10, 100, 23))
            button.setObjectName("pushButton")
            button.setText(rapport)
            self.addButton(button, index)

        self.buttonClicked.connect(self.exporteer_rapport)

    def exporteer_rapport(self, button):
        csv(button.text(), self.rapporten[button.text()])
