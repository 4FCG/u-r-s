# Probeer om de "PyQt5"-module te importeren.
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError:
    # Plaats een melding in het logbestand en toon deze in de CLI.
    print(log('MODULES', "Missende module: Python-module 'PyQt5' is vereist voor dit programma. Installeert u alstublieft de 'PyQt5'-module met het commando: 'pip install PyQt5'"))
    exit()

from lib_database import get_data
from lib_database import wijzigingen_doorvoeren
from lib_checkinput import check_input
from lib_error import error

# columns: {'columnname': locked/editable}
# change mysql table to name every tables primary key tablename_id


class Edit_table(QtWidgets.QTableWidget):
    def __init__(self, pushvar, tablename, columns, user, specifier=None, no_new=False):
        # Deze functie tekent het venster.
        super().__init__(pushvar)
        self.no_new = no_new
        self.specifier = specifier
        self.tablename = tablename.lower()
        columns[(self.tablename + '_id')] = 'locked'
        self.columns = columns
        self.columnnames = list(self.columns.keys())
        self.disabled = False
        self.user = user
        self.changelog = []
        self.setColumnCount(len(columns))
        for index, name in enumerate(self.columnnames):
            self.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(name))
        self.itemChanged.connect(self.new_data)

        # aanmaken verwijder knop
        self.pushButton = QtWidgets.QPushButton(pushvar)
        self.pushButton.setGeometry(QtCore.QRect(10, 320, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Verwijderen")
        self.pushButton.clicked.connect(self.delete_row)

        # aanmaken opslaan knop
        self.pushButton2 = QtWidgets.QPushButton(pushvar)
        self.pushButton2.setGeometry(QtCore.QRect(101, 320, 81, 23))
        self.pushButton2.setObjectName("pushButton")
        self.pushButton2.setText("Opslaan")
        self.pushButton2.clicked.connect(self.messagebox)

        # Roept de "load_data()" functie aan om zo data op te halen uit de database server.
        self.load_data()

        # Roep de "build_table()" functie aan om de tabel te vullen met de opgehaalde data.
        self.build_table()

    def load_data(self):
        # Deze functie vult de tabel met data uit de databaseserver.
        self.data = get_data(self.tablename.upper(), self.specifier)

    def build_table(self):
        # Deze functie vult de tabel met de opgehaalde data.

        # Zorgt er voor dat er tijdens het ophalen van data geen nieuwe data kan worden toegevoegd vanuit een andere functie.
        self.disabled = True

        # Zet het aantal rijen dat getekend moet worden op de lengte van de data met daarbij een 1 opgeteld.
        # Controleer of er geen nieuwe rij gemaakt dient te worden.
        if self.no_new:
            # Maak genoeg lege rijen aan voor alle data
            self.setRowCount(len(self.data))
        else:
            # Maak genoeg lege rijen aan voor alle data + 1 extra rij. Vul de primairesleutel kolom met een '*' ( om aan te geven dat deze nog niet aangemaakt is)
            self.setRowCount(len(self.data) + 1)
            self.data.append({name: '*' if self.columns[name] !=
                              'editable' else None for name in self.columnnames})

        # Voer uit voor iedere rij:
        for row_index, row in enumerate(self.data):
            # Voer uit voor ieder item in een rij:
            for item_index, name in enumerate(self.columnnames):

                # "item" word gevuld met
                item = QtWidgets.QTableWidgetItem(
                    str(row[name])) if row[name] is not None else QtWidgets.QTableWidgetItem('')

                # Controleer of de huidige kolom staat aangegeven als "locked", indien waar sta niet toe dat gebruikers waardes invullen.
                if self.columns[name] == 'locked':
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                # Controleer of de huidige kolom staat aangegeven als "editable", indien waar sta toe dat gebruikers waardes invullen.
                elif self.columns[name] == 'editable':
                    item.setFlags(QtCore.Qt.ItemIsSelectable |
                                  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

                else:
                    # Controleer of de huidige kolom staat aangegeven als "*", indien waar sta niet toe dat gebruikers waardes invullen..
                    if item.text() == '*':
                        # Maak de waarde die getoond word in de tabel gelijk aan de waarde uit de data.
                        item.setText(self.columns[name])

                    # Sta niet toe dat gebruikers waardes mogen invullen.
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.setItem(row_index, item_index, item)
        self.resizeColumnsToContents()

        # Laat andere functies weer gebruik maken van de tabel.
        self.disabled = False

    def new_data(self, item):
        # Deze functie zorgt er voor dat de wijzigingen in de tabel worden geregistreerd.
        if not self.disabled:
            # Zorgt er voor dat er tijdens het ophalen van data geen nieuwe data kan worden toegevoegd vanuit een andere functie.
            self.disabled = True
            # Variabelen controle:
            check_input(self, item)
            # data van de rij ophalen
            item_row_data = self.get_row_data(item.row())

            # Indien de huidige rij ook de laatste rij is.
            if item.row() == self.rowCount() - 1 and not self.no_new:
                # Indien de rij niet leeg is.
                if '' not in item_row_data.values():
                    # Voeg in een nieuwe rij van "data" de gegevens van "item_row_data".
                    self.data[item.row()] = item_row_data

                    # Voeg aan het changelog een nieuwe entry toe.
                    self.changelog.append(
                        {'type': 'toevoeging', 'table': self.tablename, 'data': item_row_data})
                    # Vul de tabel met de gegevens.
                    self.build_table()
            else:
                if item_row_data[self.tablename + '_id'] == '*':

                    # Voor iedere rij in "changelog":
                    for change in self.changelog:
                        if set(change['data'].values()).issubset(self.data[item.row()]):
                            column_text = self.horizontalHeaderItem(item.column()).text()
                            self.data[item.row()][column_text] = item.text()
                            change['data'][column_text] = item.text()
                            # Stel je voor je zoekt een telefoonnummer in een telefoonboek. En je hebt het zojuist gevonden. Blijf je dan doorzoeken?
                            break
                else:
                    for change in self.changelog:
                        if change['data'][self.tablename + '_id'] == item_row_data[self.tablename + '_id']:
                            change['data'] = item_row_data
                            break
                    else:
                        # Voeg aan het changelog een nieuwe entry toe.
                        self.changelog.append(
                            {'type': 'verandering', 'table': self.tablename, 'data': item_row_data})

            # Laat andere functies weer gebruik maken van de tabel.
            self.disabled = False

    def delete_row(self):
        # Deze functie verwijderd een rij.
        # zet de delete knop uit wanneer er geen toevoegingen gemaakt mogen worden
        if not self.no_new:
            # Zorgt er voor dat er tijdens het ophalen van data geen nieuwe data kan worden toegevoegd vanuit een andere functie.
            self.disabled = True

            # Controleerd of er wel een rij is geselecteerd die bestaat. Dit kan mis gaan.
            if self.currentRow() >= 0 and self.currentRow() < self.rowCount() - 1:

                # Verwijder de huidige rij uit de "data"-list.
                self.data.pop(self.currentRow())

                item_row_data = self.get_row_data(self.currentRow())

                # Indien de waarde uit "item_row_data" gelijk is aan een "*":
                if item_row_data[self.tablename + '_id'] == '*':

                    # Voor iedere rij in "changelog":
                    for index, change in enumerate(self.changelog):

                        # Indien de huidige waarde van "data" overeenkomt met "item_row_data".
                        if change['data'] == item_row_data:
                            # Verwijder de "changelog"-entry van de huidige index.
                            self.changelog.pop(index)
                            break
                else:
                    # Voeg aan het changelog een nieuwe entry toe.
                    self.changelog.append(
                        {'type': 'verwijdering', 'table': self.tablename, 'data': item_row_data})

                # Verwijder de laatst toegevoegde waarde in de "data"-list.
                self.data.pop()

                # Roep de "build_table"-functie aan om de aanpassing door te voeren naar de tabel.
                self.build_table()

            # Laat andere functies weer gebruik maken van de tabel.
            self.disabled = False

    def messagebox(self):
        # Toont een dialoog waarmee gebruikers kunnen bevestigen of ze wel degelijk hun wijzigingen willen doorvoeren.
        msgbox = QtWidgets.QMessageBox()
        msgbox.setIcon(QtWidgets.QMessageBox.Warning)
        msgbox.setText("Weet u zeker dat u deze wijzigingen wilt doorvoeren?")
        msgbox.setWindowTitle("Waarschuwing")
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgbox.exec_()
        if msgbox.clickedButton().text() == 'OK':
            self.save()

    def save(self):
        # Voert de wijzigingen door naar de database.
        wijzigingen_doorvoeren(self.changelog)
        self.load_data()

        # Roep de "build_table()" functie aan om de tabel te vullen met de opgehaalde gegevens.
        self.build_table()

    def get_row_data(self, row):
        # Haalt de waardes op van een rij, die te zien is in de tabel.
        # "items" word gevuld met de gegevens van de huidige rij.
        items = [self.item(row, i)
                 for i in range(self.columnCount())]
        # De waardes uit items worden gekoppeld aan hun kolomnaam als sleutelwaarde
        return {self.columnnames[item.column()]: None if item is None else item.text() for item in items}
