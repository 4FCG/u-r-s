# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Gebruiker\Desktop\huiswerk\ZUYD\casus\blok 3\V5\login.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(230, 230)
        MainWindow.setWindowIcon(QtGui.QIcon('images\icon.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 180, 71, 23))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 181, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 100, 181, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 150, 181, 20))
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 181, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 181, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 181, 16))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "URS: Login"))
        self.pushButton.setText(_translate("MainWindow", "Inloggen"))
        self.label.setText(_translate("MainWindow", "Voornaam"))
        self.label_2.setText(_translate("MainWindow", "Achternaam"))
        self.label_3.setText(_translate("MainWindow", "Wachtwoord"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
