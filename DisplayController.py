from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from UI import MenuDisplay


def MenuEventHandler(arg):
    print(arg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MenuDisplay.Ui_MenuWindow(MenuEventHandler)
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec())
