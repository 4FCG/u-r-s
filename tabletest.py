# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Gebruiker\Desktop\huiswerk\ZUYD\casus\blok 3\V3\tabletest.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

fakedata = [[1, "poetsvrouw", "Kan ook een man zijn"], [
    5, "hulpverlener", "Helpt met iets ofzo"], [8, "nevan", "Een homo"]]
# {'type': 'delete', 'data': []}
changelog = []


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(575, 525)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.tablename = "ACTIVITEITEN"
        self.tableWidget.setGeometry(QtCore.QRect(20, 10, 400, 471))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem("omschrijving")
        self.tableWidget.setHorizontalHeaderItem(2, item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 575, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.tableWidget.disabled = False

        # fill with data
        self.build_table()

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(410, 20, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Delete")
        self.pushButton.clicked.connect(self.delete_row)

        # event handler

        self.tableWidget.itemChanged.connect(self.new_data)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "activiteitnaam"))

    def build_table(self):
        # blank last row
        self.tableWidget.setRowCount(len(fakedata) + 1)
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1,
                                     i, None)
        # id input disabled
        item = QtWidgets.QTableWidgetItem("*")
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget.setItem(len(fakedata), 0, item)

        for index, row in enumerate(fakedata):
            item = QtWidgets.QTableWidgetItem(str(row[0]))
            # disable edit
            item.setFlags(QtCore.Qt.NoItemFlags)
            self.tableWidget.setItem(index, 0, item)
            self.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(index, 2, QtWidgets.QTableWidgetItem(row[2]))

    def new_data(self, item):
        if not self.tableWidget.disabled:
            self.tableWidget.disabled = True
            if item.row() == self.tableWidget.rowCount() - 1:
                items = []
                for i in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(item.row(), i)
                    if item is None:
                        break
                    items.append(item)
                else:
                    fakedata.append([item.text() for item in items])
                    changelog.append(
                        {'type': 'toevoeging', 'table': self.tableWidget.tablename, 'data': {self.tableWidget.horizontalHeaderItem(item.column()).text(): item.text() for item in items}})
                    self.build_table()
            else:
                items = [self.tableWidget.item(item.row(), i)
                         for i in range(self.tableWidget.columnCount())]
                if items[0].text() == '*':
                    for change in changelog:
                        if set(fakedata[item.row()]) == set(change['data'].values()):
                            fakedata[item.row()][item.column()] = item.text()
                            change['data'][self.tableWidget.horizontalHeaderItem(
                                item.column()).text()] = item.text()
                            break
                else:
                    item_row_data = {self.tableWidget.horizontalHeaderItem(
                        item.column()).text(): item.text() for item in items}
                    for change in changelog:
                        if change['data']['id'] == items[0].text():
                            change['data'] = item_row_data
                            break
                    else:
                        changelog.append(
                            {'type': 'verandering', 'table': self.tableWidget.tablename, 'data': item_row_data})
            self.tableWidget.disabled = False

    def delete_row(self):
        self.tableWidget.disabled = True
        if self.tableWidget.currentRow() >= 0 and self.tableWidget.currentRow() < self.tableWidget.rowCount() - 1:
            fakedata.pop(self.tableWidget.currentRow())

            items = [self.tableWidget.item(self.tableWidget.currentRow(), i)
                     for i in range(self.tableWidget.columnCount())]

            if items[0].text() == '*':
                for index, change in enumerate(changelog):
                    if change['data'] == {self.tableWidget.horizontalHeaderItem(item.column()).text(): item.text() for item in items}:
                        changelog.pop(index)
                        break
            else:
                changelog.append({'type': 'verwijdering', 'table': self.tableWidget.tablename, 'data': {
                                 self.tableWidget.horizontalHeaderItem(item.column()).text(): item.text() for item in items}})

            self.build_table()
        self.tableWidget.disabled = False

    def save_changes(self):
        # changelog naar riks ding
        # fakedata opniew laden uit database met laad functie
        pass

    # def toggle_weekslot(self, item):
    #     if item.column() == 2:
    #         fakedata[item.row()][item.column()] = 0 if fakedata[item.row()
    #                                                             ][item.column()] == 1 else 1
    #         self.build_table()
    # item = QtWidgets.QTableWidgetItem(
    #     "gesloten" if row[2] == 1 else "open")
    # item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
    # self.tableWidget.setItem(index, 2, item)
    # self.tableWidget.itemDoubleClicked.connect(self.toggle_weekslot)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
