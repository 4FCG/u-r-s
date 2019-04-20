import widget_login
import mainwindow
import lib_database
from lib_log import log
from lib_error import error
import sys

# Probeer om de "PyQt5"-module te importeren.
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError:
    # Plaats een melding in het logbestand en toon deze in de CLI.
    print(log('MODULES', "Missende module: Python-module 'PyQt5' is vereist voor dit programma. Installeert u alstublieft de 'PyQt5'-module met het commando: 'pip install PyQt5'"))
    exit()


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
