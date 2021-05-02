"""
    :package:   Hestia
    :file:      loginWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the login window based on QtWidgets.  
"""
import os

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

from .ui.widgets.lineEdit   import LineEdit
from .ui.widgets.iconButton import IconButton

class LoginWindow(QWidget):
    """Login Window class.

    Args:
        manager (class: "Manager"): Manager of Hestia.
        mainWindow (class: "MainWindow"): Main window of Hestia to show on login.
        winW (int, optional): Window width. Defaults to 240.
        winH (int, optional): Window height. Defaults to 320.
        parent (class: "QtWidgets", optional): PyQt parent. Defaults to None.
    """
    def __init__(self, manager, mainWindow, winW = 330, winH = 240, parent=None):
        super(LoginWindow, self).__init__(parent=parent)
        self.__manager      = manager
        self.__mainWindow   = mainWindow
        self.__service      = self.__manager.mode

        # Getting data from preferences.
        self.api            = self.__manager.link.api
        self.username       = self.__manager.preferences.getValue("MANAGER", "onlineUsername")
        self.isRememberLogin = bool(int(self.__manager.preferences.getValue("MANAGER", "rememberLogin")))

        # Set window preferences.
        self.__windowWidth = winW
        self.__windowHeight = winH

        self.__rootPath = os.path.dirname(os.path.abspath(__file__))

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
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        
        self.resize(self.__windowWidth, self.__windowHeight)

        # Set the window style.
        self.setStyle(QStyleFactory.create("Fusion"))

        # Set the main layout component.
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(10)

        # Create the api input.
        self.api = LineEdit(name="API", description="Api to connect", defaultValue=self.api)
        self.mainLayout.addWidget(self.api, 0, 0)

        # Create the username input.
        self.username = LineEdit(name="Username", description="Username", defaultValue=self.username)
        self.mainLayout.addWidget(self.username, 1, 0)

        # Create the password input.
        self.password = LineEdit(name="Password", description="Password", defaultValue="", isPassword=True)
        self.mainLayout.addWidget(self.password, 2, 0)

        # Create the save checkbox.
        self.rememberLogin = QCheckBox("Remember login")
        self.rememberLogin.setChecked(self.isRememberLogin)
        self.mainLayout.addWidget(self.rememberLogin, 3, 0)

        # Create the error window label.
        self.errorLabel = QLabel("Login failed, please verify your login informations.")
        self.errorLabel.hide()
        self.mainLayout.addWidget(self.errorLabel, 4, 0)

        # Create the login button.
        self.loginButton = IconButton(name="Login", description="Login", iconPath=self.__rootPath + "/ui/icons/check-square-fill.svg", iconScale=64, status=1, functionToInvoke=self.login)
        self.mainLayout.addWidget(self.loginButton, 5, 0)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def login(self):
        """Login to service.
        """
        # Save user preferences.
        if(self.rememberLogin.checkState() == Qt.Checked):
            self.__manager.preferences.setValue("MANAGER", "onlineHost", self.api.currentValue)
            self.__manager.preferences.setValue("MANAGER", "onlineUsername", self.username.currentValue)
            self.__manager.preferences.setValue("MANAGER", "rememberLogin", 1)
        else:
            self.__manager.preferences.setValue("MANAGER", "onlineHost", "")
            self.__manager.preferences.setValue("MANAGER", "onlineUsername", "")
            self.__manager.preferences.setValue("MANAGER", "rememberLogin", 0)
        
        self.__manager.preferences.savePreferences()

        # Connecting to online service.
        self.__connection = self.__manager.connectToOnline(api=self.api.currentValue, username=self.username.currentValue, password=self.password.currentValue)

        if (self.__connection):
            # Close this window.
            self.hide()
            self.__mainWindow.updateLog(text="Login done: %s (%s)" % (self.username.currentValue, self.__service))
            self.__mainWindow.refresh()
            self.close()
        else:
            self.errorLabel.show()