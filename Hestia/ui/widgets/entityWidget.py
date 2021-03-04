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
    """Entity widget display class.

        Args:
            name (str, optional): [description]. Defaults to "".
            description (str, optional): [description]. Defaults to "".
            iconPath (str, optional): [description]. Defaults to "".
            iconSize (int, optional): [description]. Defaults to 64.
            status (int, optional): [description]. Defaults to 1.
            versionList (list, optional): [description]. Defaults to [].
            parent ([type], optional): [description]. Defaults to None.
    """
    def __init__(self, name="", description="", iconPath="", iconSize=64, status=1, versionList=[], parent=None):
        super(EntityWidget, self).__init__(parent=parent)

        self.__defaultIcon = "./ui/icons/receipt.svg"

        self.name           = name
        self.description    = description
        self.icon           = iconPath if path.exists(iconPath) else self.__defaultIcon
        self.iconSize       = iconSize
        self.status         = status
        self.versions       = versionList

        self.initUI()
    
    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Vertical.
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.groupBox = QtWidgets.QGroupBox(self.name)
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0,0,0,0)

        # Button / Logo.
        self.iconButton = IconButton(self.name, self.description, self.icon, self.iconSize, self.status, self.importAsset)
        self.verticalLayout.addWidget(self.iconButton)

        # Version.
        self.versionDropDown = DropDown("Version", "Current version of the asset", self.getVersionsNames(), 1)
        self.verticalLayout.addWidget(self.versionDropDown)

        self.verticalLayout.addStretch(1)

        # Add the main layout to the window.
        self.groupBox.setLayout(self.verticalLayout)
        self.mainLayout.addWidget(self.groupBox)
        self.setLayout(self.mainLayout)
    
    def importAsset(self):
        """Function that invoke the import in core.
        """
        print("Import %s" % self.name)
    
    def getVersionsNames(self):
        """Getting versions names from version class.

        Returns:
            list:str: Names.
        """
        versionsNames = []
        for version in self.versions:
            versionsNames.append(version.name)
        
        if(len(versionsNames) == 0):
            return ["No versions available."]

        return versionsNames