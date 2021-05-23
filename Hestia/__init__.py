"""
    :package:   Hestia
    :file:      __init__.py
    :brief:     Initialize file.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
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

    from Hestia.core.manager    import Manager
    from Hestia.mainWindow      import MainWindow

    app = QApplication(sys.argv)

    manager = Manager(integration="standalone")

    window = MainWindow(manager=manager)
    window.show()

    sys.exit(app.exec_()) 
