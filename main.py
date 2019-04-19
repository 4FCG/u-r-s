import widget_login
import mainwindow
import lib_database
from lib_log import log
from lib_error import error
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class Loginscherm(widget_login.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(MainWindow)
        self.pushButton.clicked.connect(self.login)

    def login(self):
        log("ALGEMEEN", "[+] Succesvol opgestart!")
        loginresult = lib_database.login(self.lineEdit.text(
        ), self.lineEdit_2.text(), self.lineEdit_3.text())
        if loginresult:
            mainscreen = mainwindow.Ui_MainWindow(loginresult)
            mainscreen.setupUi(MainWindow)
        else:
            error("Incorrecte inloggegevens", "Een van de inloggegevens is incorrect!",
                        "Controleert u alstublieft of alle ingevoerde gegevens correct zijn. Neem anders contact op met het ICT-servicedesk.")

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

scherm = Loginscherm()

MainWindow.show()
sys.exit(app.exec_())
