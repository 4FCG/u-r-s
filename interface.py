import login
import tabtest
import dbtest
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


def foutmelding(title, text, informativetext):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setText(text)
    msg.setInformativeText(informativetext)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


class Loginscherm(login.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(MainWindow)
        self.pushButton.clicked.connect(self.login)



    def login(self):
        loginresult = dbtest.login(self.lineEdit.text(
        ), self.lineEdit_2.text(), self.lineEdit_3.text())
        if loginresult:
            mainscreen = tabtest.Ui_MainWindow(loginresult)
            mainscreen.setupUi(MainWindow)
        else:
            foutmelding("Incorrecte inloggegevens", "Een van de inloggegevens is incorrect", "Controleert u alstublieft of alle ingevoerde gegevens correct zijn. Neem anders contact op met het ICT-servicedesk.")


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

scherm = Loginscherm()

MainWindow.show()
sys.exit(app.exec_())
