# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Gebruiker\Desktop\huiswerk\ZUYD\casus\blok 3\V5\tabtest.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from edit_table_widget import Edit_table


class Popup(QtWidgets.QMainWindow):
    def __init__(self, werkdag_id):
        super().__init__()
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setGeometry(QtCore.QRect(10, 10, 765, 600))
        self.tableWidget = Edit_table(self.centralwidget, 'activiteit', {
                                      'starttijd': 'editable', 'uren': 'editable', 'activiteiten_id': 'editable', 'opmerking': 'editable'}, specifier="WHERE werkdag_id =" + werkdag_id + ";")
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 765, 300))
        self.tableWidget.setObjectName("tableWidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 320, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Delete")
        self.pushButton.clicked.connect(self.tableWidget.delete_row)


class Werkdag(Edit_table):
    def __init__(self, pushvar, tablename, columns, specifier=None):
        super().__init__(pushvar, tablename, columns, specifier=None)
        self.itemDoubleClicked.connect(self.dubbelklik)

    def dubbelklik(self, item):
        items = [self.item(self.currentRow(), i)
                 for i in range(self.columnCount())]
        item_row_data = {self.columnnames[item.column(
        )]: None if item is None else item.text() for item in items}

        if item_row_data['dag_id'] != '*':
            self.newscreen = Popup(item_row_data['dag_id'])
            self.newscreen.show()


class Ui_MainWindow(object):
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

        self.tableWidget = Edit_table(self.tab, 'activiteiten', {
                                      'activiteitnaam': 'editable', 'omschrijving': 'editable'})
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 765, 300))
        self.tableWidget.setObjectName("tableWidget")

        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(410, 20, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Delete")
        self.pushButton.clicked.connect(self.tableWidget.delete_row)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        # , specifier="WHERE medewerker_id =" + "'9'" + ";"
        self.tableWidget2 = Werkdag(self.tab_2, 'dag', {
            'datum': 'editable', 'starttijd': 'editable', 'eindtijd': 'editable', 'goedgekeurd': 'editable'})
        self.tableWidget2.setGeometry(QtCore.QRect(10, 10, 600, 300))
        self.tableWidget2.setObjectName("tableWidget2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab), _translate("MainWindow", "Activiteiten"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  _translate("MainWindow", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
