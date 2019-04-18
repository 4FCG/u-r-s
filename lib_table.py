from PyQt5 import QtCore, QtWidgets
from lib_database import get_data
from lib_database import rij_toevoegen
from lib_database import rij_verwijder
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
        if self.no_new:
            self.setRowCount(len(self.data))
        else:
            self.setRowCount(len(self.data) + 1)
            self.data.append({name: '*' if self.columns[name] !=
                              'editable' else None for name in self.columnnames})

        # Voer uit voor iedere rij:
        for row_index, row in enumerate(self.data):
            # Voer uit voor ieder item in een rij:
            for item_index, name in enumerate(self.columnnames):

                # "item" word gevuld met
                item = QtWidgets.QTableWidgetItem(str(row[name]) if row[name] is not None else None)

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

            # this is done twice, function?
            items = [self.item(item.row(), i)
                     for i in range(self.columnCount())]
            item_row_data = {self.columnnames[item.column(
            )]: None if item is None else item.text() for item in items}

            # Indien de huidige rij ook de laatste rij is.
            if item.row() == self.rowCount() - 1 and not self.no_new:
                # Indien de rij niet leeg is.
                if '' not in item_row_data.values():
                    # Voeg in een nieuwe rij van "data" de gegevens van "item_row_data".
                    self.data[item.row()] = item_row_data

                    # Voeg aan het changelog een nieuwe entry toe.
                    self.changelog.append(
                        {'type': 'toevoeging', 'table': self.tablename, 'data': item_row_data})
                    print('lez go boiz')
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

        # Zorgt er voor dat er tijdens het ophalen van data geen nieuwe data kan worden toegevoegd vanuit een andere functie.
        self.disabled = True

        # Controleerd of er wel een rij is geselecteerd die bestaat. Dit kan mis gaan.
        if self.currentRow() >= 0 and self.currentRow() < self.rowCount() - 1:

            # Verwijder de huidige rij uit de "data"-list.
            self.data.pop(self.currentRow())

            # "items" word gevuld met de gegevens van de huidige rij.
            items = [self.item(self.currentRow(), i)
                     for i in range(self.columnCount())]

            # "item_row_data" word gevuld met
            item_row_data = {self.columnnames[item.column(
            )]: None if item is None else item.text() for item in items}

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

    def save(self):
        # Slaat de ingevoerde gegevens op in de database. En werkt de tabel bij.
        live = 0
        print(self.changelog)
        for row in self.changelog:
            if (row['data']['dag_id'] != "*") and (row['type'] == "verwijdering"):
                if live == 1:
                    rij_verwijder("DAG", "dag_id", row['data']['dag_id'])
                    rij_verwijder("ACTIVITEIT", "werkdag_id", row['data']['dag_id'])

                else:
                    print("Verwijderen!")

            elif row['type'] == "toevoeging":
                if live == 1:
                    rij_toevoegen("DAG", ("datum", "medewerker_id", "thuisofkantoor", "starttijd", "eindtijd"), (
                        row['data']['datum'], row['data']['medewerker_id'], row['data']['thuisofkantoor'], row['data']['starttijd'], row['data']['eindtijd']))
                else:
                    print("Toevoegen!")

            elif row['type'] == "verandering":
                if live == 1:
                    rij_bijwerken("DAG", ("datum", "medewerker_id", "thuisofkantoor", "starttijd", "eindtijd"), (
                        row['data']['datum'], row['data']['medewerker_id'], row['data']['thuisofkantoor'], row['data']['starttijd'], row['data']['eindtijd']))
                else:
                    print("Bijwerken!")

        # Roep de "load_data()" functie aan om nieuwe gegevens uit de database te halen.
        self.load_data()

        # Roep de "build_table()" functie aan om de tabel te vullen met de opgehaalde gegevens.
        self.build_table()
