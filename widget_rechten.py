# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Rik\Desktop\Python programma\widget_rechten.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError:
    print(log('MODULES', "[!] Missende module: Python-module 'PyQt5' is vereist voor dit programma. Installeert u alstublieft de 'PyQt5'-module met het commando: 'pip install PyQt5'"))
    exit()


class Ui_widget_rechten(object):
    def setupUi(self, widget_rechten):
        widget_rechten.setObjectName("widget_rechten")
        widget_rechten.resize(400, 374)
        widget_rechten.setMinimumSize(QtCore.QSize(400, 374))
        widget_rechten.setMaximumSize(QtCore.QSize(400, 374))
        self.pushButton_opslaan = QtWidgets.QPushButton(widget_rechten)
        self.pushButton_opslaan.setGeometry(QtCore.QRect(220, 340, 75, 23))
        self.pushButton_opslaan.setObjectName("pushButton_opslaan")
        self.pushButton_annuleren = QtWidgets.QPushButton(widget_rechten)
        self.pushButton_annuleren.setGeometry(QtCore.QRect(310, 340, 75, 23))
        self.pushButton_annuleren.setObjectName("pushButton_annuleren")
        self.tableWidget_rechten = QtWidgets.QTableWidget(widget_rechten)
        self.tableWidget_rechten.setGeometry(QtCore.QRect(10, 60, 381, 271))
        self.tableWidget_rechten.setObjectName("tableWidget_rechten")
        self.tableWidget_rechten.setColumnCount(0)
        self.tableWidget_rechten.setRowCount(0)
        self.comboBox_functie = QtWidgets.QComboBox(widget_rechten)
        self.comboBox_functie.setGeometry(QtCore.QRect(58, 20, 331, 22))
        self.comboBox_functie.setObjectName("comboBox_functie")
        self.label_functie = QtWidgets.QLabel(widget_rechten)
        self.label_functie.setGeometry(QtCore.QRect(10, 20, 51, 21))
        self.label_functie.setObjectName("label_functie")

        self.retranslateUi(widget_rechten)
        QtCore.QMetaObject.connectSlotsByName(widget_rechten)

    def retranslateUi(self, widget_rechten):
        _translate = QtCore.QCoreApplication.translate
        widget_rechten.setWindowTitle(_translate("widget_rechten", "URS: Rechten aanpassen"))
        self.pushButton_opslaan.setText(_translate("widget_rechten", "Opslaan"))
        self.pushButton_annuleren.setText(_translate("widget_rechten", "Annuleren"))
        self.label_functie.setText(_translate("widget_rechten", "Functie:"))

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_rechten = QtWidgets.QWidget()
    ui = Ui_widget_rechten()
    ui.setupUi(widget_rechten)
    widget_rechten.show()
    sys.exit(app.exec_())

