import login
import tabletest
import dbtest
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Loginscherm(login.Ui_MainWindow):
    def login(self):
        if dbtest.login(self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text()):
            scherm2.setupUi(MainWindow)
        else:
            print("WONG")


class Activiteitenscherm(tabletest.Ui_MainWindow):
    pass


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

scherm = Loginscherm()
scherm.setupUi(MainWindow)

scherm2 = Activiteitenscherm()

MainWindow.show()
sys.exit(app.exec_())
