"""
    :package:   Hestia
    :file:      entityWidget.py
    :brief:     Entity widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from os import path

from Qt import QtWidgets, QtCore

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
    def __init__(self, manager=None, asset=None, iconSize=64, status=1, parent=None):
        super(EntityWidget, self).__init__(parent=parent)
        self.__manager  = manager
        self.__asset    = asset
        
        self.__rootPath = path.dirname(path.abspath(__file__))

        self.__defaultIcon = self.__rootPath + "/../icons/card-image.svg"

        self.__name           = asset.name
        self.__description    = asset.description
        self.__icon           = asset.icon if path.exists(asset.icon) else self.__defaultIcon
        self.__iconSize       = iconSize
        self.__versions       = asset.versions
        self.__currentVersion = self.__versions[0] if len(self.__versions) > 0 else None

        if(len(self.__versions) > 0):
            self.__status = 0 if not self.__currentVersion.type in self.__manager.integration.availableFormats else 1
        else:
            self.__status = 0

        self.initUI()
    
    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Vertical.
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.groupBox = QtWidgets.QGroupBox(self.__name)
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0,0,0,0)

        # Button / Logo.
        self.iconButton = IconButton(self.__name, self.__description, self.__icon, self.__iconSize, self.__status, self.importAsset)
        self.verticalLayout.addWidget(self.iconButton)

        # Version. > Refresh bug here.
        self.versionDropDown = DropDown(name="Version",
                                        description="Current version of the asset",
                                        datas=self.getVersionsNames(),
                                        defaultValue=0,
                                        functionToInvoke=self.updateEntity)
        self.verticalLayout.addWidget(self.versionDropDown)

        self.verticalLayout.addStretch(1)

        # Add the main layout to the window.
        self.groupBox.setLayout(self.verticalLayout)
        self.mainLayout.addWidget(self.groupBox)
        self.setLayout(self.mainLayout)

    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                currentProject = self.__manager.projects[self.__manager.currentProject]
                print("Right button clicked on %s [%s] ! @ %s" % (self.__name, currentProject.categories[currentProject.currentCategory].type, event.globalPos()))
                # TODO: Create a floating widget at the global position with additional features.

    
    def importAsset(self):
        """Function that invoke the import in core.
        """
        self.__manager.logging.info("Import %s" % self.__name)
        
        currentProject = self.__manager.projects[self.__manager.currentProject]

        if(currentProject.categories[currentProject.currentCategory].type == "Assets"):
            self.__manager.integration.loadAsset(asset = self.__asset,
                                                version = self.__currentVersion)

        elif(currentProject.categories[currentProject.currentCategory].type == "Shots"):
            self.__manager.integration.loadShot(asset = self.__asset,
                                                version = self.__currentVersion)

        else:
            self.__manager.logging.error("Load failed: not supported type.")
    
    def getVersionsNames(self):
        """Getting versions names from version class.

        Returns:
            list:str: Names.
        """
        versionsNames = []
        for version in self.__versions:
            versionsNames.append("%s (%s)" % (version.name, version.type))
        
        if(len(versionsNames) == 0):
            return ["No versions available."]

        return versionsNames

    def updateEntity(self):
        """Update the entity widget with the new selected version.
        """
        if(len(self.__versions) > 0):
            self.__currentVersion = self.__versions[self.versionDropDown.currentValue]

            self.__status = 0 if not self.__currentVersion.type in self.__manager.integration.availableFormats else 1
            self.iconButton.changeButtonStatus(self.__status)