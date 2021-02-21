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
    def __init__(self, parent=None):
        """header Class.

        Args:
            parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
        """
        super(Header, self).__init__(parent=parent)

        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the main layout component.
        self.mainLayout = QtWidgets.QHBoxLayout()

        # Add import as instance checkbox.
        self.importAsInstance = QtWidgets.QCheckBox("Instance")
        self.importAsInstance.setToolTip("Import the asset as instance in the scene.")
        self.importAsInstance.setChecked(True)
        self.mainLayout.addWidget(self.importAsInstance)

        # Add spacer to header.
        self.mainLayout.addStretch()

        # Add project selector to header.
        self.projectSelector = DropDown("Project", "Current project", ["Demo"])
        self.mainLayout.addWidget(self.projectSelector)

        #TODO: ADD PREFERENCES.
        # Add preference button.
        #self.preferenceButton = QtWidgets.QPushButton("Preferences")
        #self.mainLayout.addWidget(self.preferenceButton)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)