# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Gebruiker\Desktop\huiswerk\ZUYD\casus\blok 3\V5\tabtest.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

# Probeer om de "PyQt5"-module te importeren.
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError:
    # Plaats een melding in het logbestand en toon deze in de CLI.
    print(log('MODULES', "Missende module: Python-module 'PyQt5' is vereist voor dit programma. Installeert u alstublieft de 'PyQt5'-module met het commando: 'pip install PyQt5'"))
    exit()

from lib_table import Edit_table
from widget_rapport import Rapport_buttons


class Popup(QtWidgets.QMainWindow):
    def __init__(self, werkdag_id, datum, user, no_new=False):
        super().__init__()

        # Venster: Uiterlijk
        self.setFixedSize(800, 370)
        self.setWindowTitle("URS: Uren aanpassen voor " + datum)
        self.setWindowIcon(QtGui.QIcon('images\icon.png'))
        self.no_new = no_new
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setGeometry(QtCore.QRect(10, 10, 765, 600))
        self.tableWidget = Edit_table(self.centralwidget, 'activiteit', {
                                      'starttijd': 'editable', 'uren': 'editable', 'activiteiten_id': 'editable', 'opmerking': 'editable', 'werkdag_id': werkdag_id}, user, specifier="WHERE werkdag_id =" + werkdag_id + ";", no_new=self.no_new)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 765, 300))
        self.tableWidget.setObjectName("tableWidget")


class Werkdag(Edit_table):
    def __init__(self, pushvar, tablename, columns, user, specifier=None, no_new=False):
        super().__init__(pushvar, tablename, columns, user, specifier, no_new)
        self.itemDoubleClicked.connect(self.dubbelklik)
        self.inlogdata = user
        self.no_new = no_new

    def dubbelklik(self, item):
        item_row_data = self.get_row_data(item.row())

        if item_row_data['dag_id'] != '*':
            self.newscreen = Popup(
                item_row_data['dag_id'], item_row_data['datum'], self.inlogdata, no_new=self.no_new)
            self.newscreen.show()


class Werkdagen_popup(QtWidgets.QMainWindow):
    def __init__(self, medewerker_id, user):
        super().__init__()
        self.setFixedSize(600, 600)
        self.setWindowTitle("URS: Dagen aanpassen")
        self.setWindowTitle("URS: Dagen aanpassen")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setGeometry(QtCore.QRect(10, 10, 765, 600))
        self.tableWidget = Werkdag(self.centralwidget, 'dag', {
            'datum': 'locked', 'thuisofkantoor': 'locked', 'starttijd': 'locked', 'eindtijd': 'locked', 'goedgekeurd': 'editable', 'medewerker_id': 'locked'}, user, specifier="WHERE medewerker_id =" + medewerker_id + ";", no_new=True)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 765, 300))
        self.tableWidget.setObjectName("tableWidget")


class Medewerker_overzicht(Edit_table):
    def __init__(self, pushvar, tablename, columns, user, specifier=None, no_new=False):
        super().__init__(pushvar, tablename, columns, user, specifier, no_new)
        self.itemDoubleClicked.connect(self.dubbelklik)
        self.inlogdata = user

    def dubbelklik(self, item):
        item_row_data = self.get_row_data(item.row())

        if item_row_data['medewerker_id'] != '*':
            self.newscreen = Werkdagen_popup(item_row_data['medewerker_id'], self.inlogdata)
            self.newscreen.show()


class Ui_MainWindow(object):
    def __init__(self, inlogdata):
        super().__init__()
        self.inlogdata = inlogdata
        self.buttons = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Urenregistratiesysteem v1.0")
        MainWindow.setFixedSize(788, 400)
        MainWindow.setWindowIcon(QtGui.QIcon('images\icon.png'))
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Urenregistratie")
        self.tableWidget2 = Werkdag(self.tab_2, 'dag', {
            'datum': 'editable', 'thuisofkantoor': 'editable', 'starttijd': 'editable', 'eindtijd': 'editable', 'goedgekeurd': '0', 'medewerker_id': str(self.inlogdata['medewerker_id'])}, self.inlogdata, specifier="WHERE medewerker_id =" + str(self.inlogdata['medewerker_id']) + ";")
        self.tableWidget2.setGeometry(QtCore.QRect(10, 10, 765, 300))
        self.tableWidget2.setObjectName("tableWidget2")

        # manager only functies
        if self.inlogdata['manager_id'] is None:
            # uren goedkeuren
            self.tab_3 = QtWidgets.QWidget()
            self.tab_3.setObjectName("tab_3")
            self.tabWidget.addTab(self.tab_3, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(
                self.tab_3), "Uren goedkeuren")
            self.tableWidget3 = Medewerker_overzicht(self.tab_3, 'medewerker', {
                'voornaam': 'locked', 'achternaam': 'locked', 'functie_id': 'editable', 'manager_id': 'locked', 'weekslot': 'editable'}, self.inlogdata, specifier="WHERE manager_id =" + str(self.inlogdata['medewerker_id']) + ";", no_new=True)
            self.tableWidget3.setGeometry(QtCore.QRect(10, 10, 765, 300))
            self.tableWidget3.setObjectName("tableWidget3")

            # activiteiten aanpassen
            self.tabWidget.addTab(self.tab, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(
                self.tab), "Activiteiten")
            self.tableWidget = Edit_table(self.tab, 'activiteiten', {
                                          'activiteitnaam': 'editable', 'omschrijving': 'editable'}, self.inlogdata)
            self.tableWidget.setGeometry(QtCore.QRect(10, 10, 765, 300))
            self.tableWidget.setObjectName("tableWidget")

            # raport data generatie
            self.tab_4 = QtWidgets.QWidget()
            self.tab_4.setObjectName("tab_3")
            self.tabWidget.addTab(self.tab_4, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(
                self.tab_4), "Rapport data")

            self.buttons = Rapport_buttons(self.tab_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
