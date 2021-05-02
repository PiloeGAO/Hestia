"""
    :package:   Hestia
    :file:      header.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
    :brief:     Class to create the header of the window.  
"""
import os

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

from .widgets.dropDown      import DropDown
from .widgets.iconButton    import IconButton

class Header(QWidget):
    def __init__(self, manager, mainWindow, parent=None):
        """header Class.

        Args:
            manager (class: "Manager"): The Hestia manager.
            mainWindow (class: "MainWindow"): The Hestia main window.
            parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
        """
        super(Header, self).__init__(parent=parent)
        self.__manager = manager
        self.__mainWindow = mainWindow
        
        self.__rootPath = os.path.dirname(os.path.abspath(__file__))

        self.importAsReferenceState = True

        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the main layout component.
        self.mainLayout = QHBoxLayout()

        # Add import as instance checkbox.
        self.importAsReference = QCheckBox("Reference")
        self.importAsReference.setToolTip("Import the asset as reference in the scene.")
        self.importAsReference.setChecked(self.importAsReferenceState)
        self.importAsReference.stateChanged.connect(self.changeImportAsReferenceState)
        self.mainLayout.addWidget(self.importAsReference)

        if(self.__manager.integration.supportInstances):
            self.importAsReference.show()
        else:
            self.importAsReference.hide()

        # Add spacer to header.
        self.mainLayout.addStretch()

        # Add project selector to header.
        self.projectSelector = DropDown(name="Project", description="Current project", datas=["Local"], functionToInvoke=self.changeProject)
        self.mainLayout.addWidget(self.projectSelector)

        # Add preference button.
        self.preferenceButton = IconButton(name="Preferences",
                                            description="Open preferences window.",
                                            iconPath=self.__rootPath + "/../ui/icons/gear.svg",
                                            iconScale=16,
                                            status=1,
                                            functionToInvoke=self.__mainWindow.openPreferencesWindow,
                                            parent=None)                                       
        self.mainLayout.addWidget(self.preferenceButton)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def changeImportAsReferenceState(self):
        """Change the state of the importAsInstance checkbox.
        """
        self.importAsReferenceState = self.importAsReference.checkState()
        self.__manager.integration.instances = self.importAsReference.isChecked()
    
    def changeProject(self):
        """Change the project on the manager and update the mainWindow.
        """
        self.__manager.currentProject = self.projectSelector.currentValue
        self.__mainWindow.refreshProject()

    def refresh(self):
        """Force refresh of the widget.
        """
        projectsName = [project.name for project in self.__manager.projects]
        self.projectSelector.datas = projectsName

        self.update()