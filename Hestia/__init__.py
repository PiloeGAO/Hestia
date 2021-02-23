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

    username = input("username: ")
    password = input("password: ")

    manager = Manager()
    manager.connectToOnline(api="https://pole3d.cg-wire.com/api/", username=username, password=password)

    app = QtWidgets.QApplication(sys.argv)

    login = LoginWindow(manager=manager)
    login.show()

    window = MainWindow(manager=manager)
    window.show()

    sys.exit(app.exec_()) 
