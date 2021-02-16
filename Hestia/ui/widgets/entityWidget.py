"""
    :package:   Hestia
    :file:      entityWidget.py
    :brief:     Entity widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

from Qt import QtWidgets

from .iconButton    import IconButton
from .dropDown      import DropDown

class EntityWidget(QtWidgets.QWidget):
    """Entity widget class.

    Args:
        parent ([type], optional): Parent widget. Defaults to None.
    """
    def __init__(self, parent=None):
        super(EntityWidget, self).__init__(parent=parent)

        self.initUI()
    
    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Vertical.
        self.mainLayout = QtWidgets.QVBoxLayout()

        # Button / Logo.
        self.iconButton = IconButton("Entity", "The entity", "", 64, 1, self.importAsset)
        self.mainLayout.addWidget(self.iconButton)

        # Name label.
        self.nameLabel = QtWidgets.QLabel("Entity")
        self.mainLayout.addWidget(self.nameLabel)

        # Version.
        self.versionDropDown = DropDown("Version", "Current version of the asset", ["001", "002"], 1)
        self.mainLayout.addWidget(self.versionDropDown)

        # Add the main layout to the window.
        self.setLayout(self.mainLayout)
    
    def importAsset(self):
        """Function that invoke the import in core.
        """
        print("Import asset")