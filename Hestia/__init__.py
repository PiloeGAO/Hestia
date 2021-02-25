"""
    :package:   Hestia
    :file:      __init__.py
    :brief:     Initialize file.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

from os import sys, path

from Qt import QtWidgets

if __name__ == "__main__":
    if __package__ is None:
        print("Not executed in package.")
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    from Hestia.mainWindow      import MainWindow

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(mode="kitsu")
    window.show()

    sys.exit(app.exec_()) 
