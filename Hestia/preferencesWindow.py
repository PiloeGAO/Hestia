"""
    :package:   Hestia
    :file:      preferencesWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
    :brief:     Class to create the preferences window based on QtWidgets.  
"""
try:
    from PySide2.QtCore     import *
    from PySide2.QtGui      import *
    from PySide2.QtWidgets  import *
except:
    from PySide.QtCore      import *
    from PySide.QtGui       import *

from .ui.widgets.gridWidget import GridWidget
from .ui.widgets.dropDown   import DropDown

class PreferencesWindow(QWidget):
    """Preferences Window class.

    Args:
        manager (class: "Manager", optional): Manager of Hestia. Defaults to Manager().
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

        # Tab manager initializer.
        self.mainLayout = QVBoxLayout()
        self.tabWidget = QTabWidget()

        # Set the main settings layout component.
        # Set service.
        self.serviceButton = DropDown(name="Service",
                                        description="Service used.",
                                        datas=self.__servicesAvailables,
                                        defaultValue=self.__currentService,
                                        functionToInvoke=None)

        # Load previews.
        self.loadPreviews = QCheckBox("Download previews")
        self.loadPreviews.setToolTip("Warning: This can slowdown the GUI.")
        self.loadPreviews.setChecked(self.__loadPreviewStatus)


        self.mainSettingsWidget = GridWidget(self.__manager, self, xSize=1, itemList=[
            self.serviceButton,
            self.loadPreviews
        ])
        self.tabWidget.addTab(self.mainSettingsWidget, "Main Settings")

        # Project manager settings.
        self.projectManagerSettingsWidget = QWidget()

        self.projectManagerSettingsLayout = QVBoxLayout()

        if(self.__manager.projects[self.__manager.currentProject].supportFileTree):
            self.buildProjectFolderTreeButton = QPushButton("Build folder tree")
            self.buildProjectFolderTreeButton.clicked.connect(self.buildProjectFolderTree)
            self.projectManagerSettingsLayout.addWidget(self.buildProjectFolderTreeButton)

        self.projectManagerSettingsWidget.setLayout(self.projectManagerSettingsLayout)
        self.tabWidget.addTab(self.projectManagerSettingsWidget, "Project Manager Settings")

        # Set main layout to the window.
        self.mainLayout.addWidget(self.tabWidget)
        
        # Save button.
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.savePreferences)
        self.mainLayout.addWidget(self.saveButton)

        self.setLayout(self.mainLayout)
    
    def buildProjectFolderTree(self):
        """Build project foldertree.
        """
        self.__manager.logging.info("Folder tree generation started.")
        self.__manager.projects[self.__manager.currentProject].buildFolderTree()
        self.__manager.logging.info("Folder tree successfully generated.")
    
    def savePreferences(self):
        """Save preferences.
        """
        self.__manager.preferences.setValue("MANAGER", "service", self.__servicesAvailables[self.serviceButton.currentValue].lower())
        self.__manager.preferences.setValue("MANAGER", "loadPreviews", str(int(self.loadPreviews.isChecked())))
        self.__manager.preferences.savePreferences()

        # Show information message.
        QMessageBox.warning(self, self.tr("Hestia"),
                            self.tr("Preferences has been modified.\n" + \
                                "Please restart Hestia."),
                            QMessageBox.NoButton,
                            QMessageBox.Ok)

        self.hide()
