"""
    :package:   Hestia
    :file:      __init__.py
    :brief:     Initialize file.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
"""

from os import sys, path

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

if __name__ == "__main__":
    if __package__ is None:
        print("Not executed in package.")
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    from Hestia.mainWindow      import MainWindow

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_()) 
