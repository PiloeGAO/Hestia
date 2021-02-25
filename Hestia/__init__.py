"""
    :package:   Hestia
    :file:      __init__.py
    :brief:     Initialize file.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

from os import sys, path

from Qt import QtWidgets, QtGui

if __name__ == "__main__":
    if __package__ is None:
        print("Not executed in package.")
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    # Core Libs.
    from Hestia.core.manager    import Manager

    # UI Libs.
    from Hestia.loginWindow     import LoginWindow
    from Hestia.mainWindow      import MainWindow
    
    manager = Manager()

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(manager=manager, mode="kitsu")
    window.show()

    sys.exit(app.exec_()) 
