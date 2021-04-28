"""
    :package:   Hestia
    :file:      preferencesWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the preferences window based on QtWidgets.  
"""
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

from .ui.widgets.dropDown   import DropDown

class PreferencesWindow(QWidget):
    """Preferences Window class.

    Args:
        manager (class: "Manager", optional): Manager of Hestia. Defaults to Manager().
        winW (int, optional): Window width. Defaults to 640.
        winH (int, optional): Window height. Defaults to 480.
        parent (class: "QtWidgets", optional): PyQt parent. Defaults to None.
    """
    def __init__(self, manager, parent=None):
        super(PreferencesWindow, self).__init__(parent=parent)
        # Defining the Manager.
        self.__manager = manager

        # Set window preferences.
        self.__windowWidth, self.__windowHeight = 640, 480

        # Manager preferences.
        serviceFromPreferences = self.__manager.preferences.getValue("MANAGER", "service")
        self.__servicesAvailables = ["Local", "Kitsu"]
        self.__currentService = [i for i,x in enumerate(self.__servicesAvailables) if x.lower() == serviceFromPreferences][0]

        self.__loadPreviewStatus = bool(int(self.__manager.preferences.getValue("MANAGER", "loadPreviews")))

        # Initialize UI.
        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """
        # Set the window title.
        self.setWindowTitle("Hestia - Preferences")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        
        # Set the window size.
        #self.resize(self.__windowWidth, self.__windowHeight)

        # Set the window style.
        self.setStyle(QStyleFactory.create("Fusion"))

        # Set the main layout component.
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(10)

        # Set window size.

        # Set service.
        self.serviceButton = DropDown(name="Service",
                                        description="Service used.",
                                        datas=self.__servicesAvailables,
                                        defaultValue=self.__currentService,
                                        functionToInvoke=None)
        
        self.mainLayout.addWidget(self.serviceButton, 0, 0)

        # Load previews.
        self.loadPreviews = QCheckBox("Download previews")
        self.loadPreviews.setToolTip("Warning: This can slowdown the GUI.")
        self.loadPreviews.setChecked(self.__loadPreviewStatus)
        self.mainLayout.addWidget(self.loadPreviews, 1, 0)

        # Save button.
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.savePreferences)
        self.mainLayout.addWidget(self.saveButton, 2, 1)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def savePreferences(self):
        """Save preferences.
        """
        self.__manager.preferences.setValue("MANAGER", "service", self.__servicesAvailables[self.serviceButton.currentValue].lower())
        self.__manager.preferences.setValue("MANAGER", "loadPreviews", str(int(self.loadPreviews.isChecked())))
        self.__manager.preferences.savePreferences()

        # Shwo information message.
        infoPopup = QMessageBox("Hestia | Warning")
        infoPopup.setText("Please restart Hestia.")
        infoPopup.exec_()

        self.hide()
