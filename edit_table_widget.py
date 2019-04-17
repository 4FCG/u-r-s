from PyQt5 import QtCore, QtWidgets
from dbtest import get_data
# columns: {'columnname': locked/editable}
# change mysql table to name every tables primary key tablename_id


class Edit_table(QtWidgets.QTableWidget):
    def __init__(self, pushvar, tablename, columns, user, specifier=None):
        super().__init__(pushvar)
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

        self.load_data()
        self.build_table()

    def load_data(self):
        self.data = get_data(self.tablename.upper(), self.specifier)

    def build_table(self):
        self.disabled = True
        self.setRowCount(len(self.data) + 1)
        self.data.append({name: '*' if self.columns[name] !=
                          'editable' else None for name in self.columnnames})

        for row_index, row in enumerate(self.data):
            for item_index, name in enumerate(self.columnnames):
                item = QtWidgets.QTableWidgetItem(str(row[name]) if row[name] is not None else None)
                if self.columns[name] == 'locked':
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                elif self.columns[name] == 'editable':
                    item.setFlags(QtCore.Qt.ItemIsSelectable |
                                  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                else:
                    if item.text() == '*':
                        item.setText(self.columns[name])
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.setItem(row_index, item_index, item)
        self.resizeColumnsToContents()

        self.disabled = False

    def new_data(self, item):
        if not self.disabled:
            self.disabled = True

            # this is done twice, function?
            items = [self.item(item.row(), i)
                     for i in range(self.columnCount())]
            item_row_data = {self.columnnames[item.column(
            )]: None if item is None else item.text() for item in items}

            if item.row() == self.rowCount() - 1:
                if '' not in item_row_data.values():
                    self.data[item.row()] = item_row_data
                    self.changelog.append(
                        {'type': 'toevoeging', 'table': self.tablename, 'data': item_row_data})
                    self.build_table()
            else:
                if item_row_data[self.tablename + '_id'] == '*':
                    for change in self.changelog:
                        if set(change['data'].values()).issubset(self.data[item.row()]):
                            column_text = self.horizontalHeaderItem(item.column()).text()
                            self.data[item.row()][column_text] = item.text()
                            change['data'][column_text] = item.text()
                            break
                else:
                    for change in self.changelog:
                        if change['data'][self.tablename + '_id'] == item_row_data[self.tablename + '_id']:
                            change['data'] = item_row_data
                            break
                    else:
                        self.changelog.append(
                            {'type': 'verandering', 'table': self.tablename, 'data': item_row_data})
            self.disabled = False

    def delete_row(self):
        self.disabled = True
        if self.currentRow() >= 0 and self.currentRow() < self.rowCount() - 1:
            self.data.pop(self.currentRow())

            # twice
            items = [self.item(self.currentRow(), i)
                     for i in range(self.columnCount())]
            item_row_data = {self.columnnames[item.column(
            )]: None if item is None else item.text() for item in items}

            if item_row_data[self.tablename + '_id'] == '*':
                for index, change in enumerate(self.changelog):
                    if change['data'] == item_row_data:
                        self.changelog.pop(index)
                        break
            else:
                self.changelog.append(
                    {'type': 'verwijdering', 'table': self.tablename, 'data': item_row_data})

            self.data.pop()
            self.build_table()
        self.disabled = False

    def save(self):
        # send changelog
        print(self.user, self.changelog)
        self.load_data()
        self.build_table()
