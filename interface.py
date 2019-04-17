import login
import tabtest
import dbtest
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


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
            print("WONG")


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

scherm = Loginscherm()

MainWindow.show()
sys.exit(app.exec_())
