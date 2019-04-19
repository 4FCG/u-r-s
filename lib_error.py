def error(title, text, informativetext):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setText(text)
    msg.setInformativeText(informativetext)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()