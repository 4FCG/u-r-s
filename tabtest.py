# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Gebruiker\Desktop\huiswerk\ZUYD\casus\blok 3\V5\tabtest.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from edit_table_widget import Edit_table


class Popup(QtWidgets.QMainWindow):
    def __init__(self, werkdag_id, user):
        super().__init__()
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setGeometry(QtCore.QRect(10, 10, 765, 600))
        self.tableWidget = Edit_table(self.centralwidget, 'activiteit', {
                                      'starttijd': 'editable', 'uren': 'editable', 'activiteiten_id': 'editable', 'opmerking': 'editable', 'werkdag_id': werkdag_id}, user, specifier="WHERE werkdag_id =" + werkdag_id + ";")
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 765, 300))
        self.tableWidget.setObjectName("tableWidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 320, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Delete")
        self.pushButton.clicked.connect(self.tableWidget.delete_row)

        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(101, 320, 81, 23))
        self.pushButton2.setObjectName("pushButton")
        self.pushButton2.setText("Opslaan")
        self.pushButton2.clicked.connect(self.tableWidget.save)


class Werkdag(Edit_table):
    def __init__(self, pushvar, tablename, columns, user, specifier=None):
        super().__init__(pushvar, tablename, columns, user, specifier)
        self.itemDoubleClicked.connect(self.dubbelklik)
        self.inlogdata = user

    def dubbelklik(self, item):
        items = [self.item(self.currentRow(), i)
                 for i in range(self.columnCount())]
        item_row_data = {self.columnnames[item.column(
        )]: None if item is None else item.text() for item in items}

        if item_row_data['dag_id'] != '*':
            self.newscreen = Popup(item_row_data['dag_id'], self.inlogdata)
            self.newscreen.show()


class Ui_MainWindow(object):
    def __init__(self, inlogdata):
        super().__init__()
        self.inlogdata = inlogdata

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 791, 551))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        # uren registratie
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Uren registratie")
        self.tableWidget2 = Werkdag(self.tab_2, 'dag', {
            'datum': 'editable', 'thuisofkantoor': 'editable', 'starttijd': 'editable', 'eindtijd': 'editable', 'goedgekeurd': '0', 'medewerker_id': str(self.inlogdata['medewerker_id'])}, self.inlogdata, specifier="WHERE medewerker_id =" + str(self.inlogdata['medewerker_id']) + ";")
        self.tableWidget2.setGeometry(QtCore.QRect(10, 10, 765, 300))
        self.tableWidget2.setObjectName("tableWidget2")

        self.pushButton2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton2.setGeometry(QtCore.QRect(10, 320, 81, 23))
        self.pushButton2.setObjectName("pushButton")
        self.pushButton2.setText("Delete")
        self.pushButton2.clicked.connect(self.tableWidget2.delete_row)

        self.pushButton3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton3.setGeometry(QtCore.QRect(101, 320, 81, 23))
        self.pushButton3.setObjectName("pushButton")
        self.pushButton3.setText("Opslaan")
        self.pushButton3.clicked.connect(self.tableWidget2.save)

        # manager only functies
        if self.inlogdata['manager_id'] is None:
            # activiteiten aanpassen
            self.tabWidget.addTab(self.tab, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(
                self.tab), "Activiteiten")
            self.tableWidget = Edit_table(self.tab, 'activiteiten', {
                                          'activiteitnaam': 'editable', 'omschrijving': 'editable'}, self.inlogdata)
            self.tableWidget.setGeometry(QtCore.QRect(10, 10, 765, 300))
            self.tableWidget.setObjectName("tableWidget")

            self.pushButton = QtWidgets.QPushButton(self.tab)
            self.pushButton.setGeometry(QtCore.QRect(10, 320, 81, 23))
            self.pushButton.setObjectName("pushButton")
            self.pushButton.setText("Delete")
            self.pushButton.clicked.connect(self.tableWidget.delete_row)

            self.pushButton4 = QtWidgets.QPushButton(self.tab)
            self.pushButton4.setGeometry(QtCore.QRect(101, 320, 81, 23))
            self.pushButton4.setObjectName("pushButton")
            self.pushButton4.setText("Opslaan")
            self.pushButton4.clicked.connect(self.tableWidget.save)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
