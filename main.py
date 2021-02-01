import sys
from Qt import QtWidgets, QtGui

from Hestia.mainWindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec_()) 
