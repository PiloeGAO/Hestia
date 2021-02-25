"""
    :package:   Hestia
    :file:      loginWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the login window based on QtWidgets.  
"""
from Qt import QtWidgets, QtCore

from .ui.widgets.lineEdit   import LineEdit
from .ui.widgets.iconButton import IconButton

class LoginWindow(QtWidgets.QWidget):
    """Login Window class.

    Args:
        manager (class: "Manager"): Manager of Hestia.
        mainWindow (class: "MainWindow"): Main window of Hestia to show on login.
        winW (int, optional): Window width. Defaults to 240.
        winH (int, optional): Window height. Defaults to 320.
        parent (class: "QtWidgets", optional): PyQt parent. Defaults to None.
    """
    def __init__(self, manager, mainWindow, service, winW = 240, winH = 320, parent=None):
        super(LoginWindow, self).__init__(parent=parent)

        self.__manager      = manager
        self.__mainWindow   = mainWindow
        self.__service      = service

        # Set window preferences.
        self.__windowWidth  = winW
        self.__windowHeight = winH

        self.__connection = None

        self.initUI()
    
    def closeEvent(self, event):
        """Close event of the login window.

        Args:
            event (class: "QtWidgets"): Window event.
        """
        if(not self.__connection):
            self.__mainWindow.close()

    def initUI(self):
        """Generate the window.
        """

        # Set the window title.
        self.setWindowTitle("Hestia - Login to %s" % self.__service)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        
        # Set the window size.
        self.resize(self.__windowWidth, self.__windowHeight)

        # Set the window style.
        self.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

        # Set the main layout component.
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setSpacing(10)

        # Create the api input.
        self.api = LineEdit(name="API", description="Api to connect", defaultValue="https://pole3d.cg-wire.com/api")
        self.mainLayout.addWidget(self.api, 0, 0)

        # Create the username input.
        self.username = LineEdit(name="Username", description="Username", defaultValue="")
        self.mainLayout.addWidget(self.username, 1, 0)

        # Create the password input.
        self.password = LineEdit(name="Password", description="Password", defaultValue="", isPassword=True)
        self.mainLayout.addWidget(self.password, 2, 0)

        # Create the erro window label.
        self.errorLabel = QtWidgets.QLabel("Login failed, please verify your login informations.")
        self.errorLabel.hide()
        self.mainLayout.addWidget(self.errorLabel, 3, 0)

        # Create the login button.
        self.loginButton = IconButton(name="Login", description="Login", iconPath="./ui/icons/check-square-fill.svg", iconScale=64, status=1, functionToInvoke=self.login)
        self.mainLayout.addWidget(self.loginButton, 4, 0)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def login(self):
        """Login to service.
        """
        self.__connection = self.__manager.connectToOnline(service=self.__service, api=self.api.currentValue, username=self.username.currentValue, password=self.password.currentValue)

        if (self.__connection):
            self.hide()
            self.__mainWindow.refresh()
            self.close()
        else:
            self.errorLabel.show()