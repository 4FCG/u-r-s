try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError:
    log('MODULES', "Missende module: Python-module 'PyQt5' is vereist voor dit programma. Installeert u alstublieft de 'PyQt5'-module met het commando: 'pip install PyQt5'")
    exit()


def error(title, text, informativetext):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setText(text)
    msg.setInformativeText(informativetext)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()