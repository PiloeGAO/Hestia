"""
    :package:   Hestia
    :file:      entityWidget.py
    :brief:     Entity widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from os import path

from Qt import QtWidgets

from .iconButton    import IconButton
from .dropDown      import DropDown

class EntityWidget(QtWidgets.QWidget):
    """Entity widget class.

    Args:
        parent ([type], optional): Parent widget. Defaults to None.
    """
    def __init__(self, name="", description="", iconPath="", iconSize=64, status=1, versionList=[], parent=None):
        super(EntityWidget, self).__init__(parent=parent)

        self.__defaultIcon = "./ui/icons/receipt.svg"

        self.name           = name
        self.description    = description
        self.icon           = iconPath if path.exists(iconPath) else self.__defaultIcon
        self.iconSize       = iconSize
        self.status         = status
        self.versions       = versionList if len(versionList)>0 else ["NO VERSION"]

        self.initUI()
    
    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Vertical.
        self.mainLayout = QtWidgets.QVBoxLayout()

        # Button / Logo.
        self.iconButton = IconButton(self.name, self.description, self.icon, self.iconSize, self.status, self.importAsset)
        self.mainLayout.addWidget(self.iconButton)

        # Name label.
        self.nameLabel = QtWidgets.QLabel(self.name)
        self.mainLayout.addWidget(self.nameLabel)

        # Version.
        self.versionDropDown = DropDown("Version", "Current version of the asset", self.versions, 1)
        self.mainLayout.addWidget(self.versionDropDown)

        # Add the main layout to the window.
        self.setLayout(self.mainLayout)
    
    def importAsset(self):
        """Function that invoke the import in core.
        """
        print("Import %s" % self.name)