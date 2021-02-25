"""
    :package:   Hestia
    :file:      header.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the header of the window.  
"""
from Qt import QtWidgets

from .widgets.dropDown      import DropDown
from .widgets.iconButton    import IconButton

class Header(QtWidgets.QWidget):
    def __init__(self, manager, parent=None):
        """header Class.

        Args:
            parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
        """
        super(Header, self).__init__(parent=parent)
        self.__manager = manager

        self.importAsInstanceState = True

        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the main layout component.
        self.mainLayout = QtWidgets.QHBoxLayout()

        # Add import as instance checkbox.
        self.importAsInstance = QtWidgets.QCheckBox("Instance")
        self.importAsInstance.setToolTip("Import the asset as instance in the scene.")
        self.importAsInstance.setChecked(self.importAsInstanceState)
        self.importAsInstance.stateChanged.connect(self.changeImportAsInstanceState)
        self.mainLayout.addWidget(self.importAsInstance)

        # Add spacer to header.
        self.mainLayout.addStretch()

        # Add project selector to header.
        self.projectSelector = DropDown("Project", "Current project", ["Local"])
        self.mainLayout.addWidget(self.projectSelector)

        #TODO: ADD PREFERENCES.
        # Add preference button.
        #self.preferenceButton = QtWidgets.QPushButton("Preferences")
        #self.mainLayout.addWidget(self.preferenceButton)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def changeImportAsInstanceState(self):
        """Change the state of the importAsInstance checkbox.
        """
        self.importAsInstanceState = self.importAsInstance.checkState()

    def refresh(self):
        """Force refresh of the widget.
        """
        projectsName = [project.name for project in self.__manager.projects]
        self.projectSelector.datas = projectsName
        self.update()