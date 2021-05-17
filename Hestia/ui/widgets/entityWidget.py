"""
    :package:   Hestia
    :file:      entityWidget.py
    :brief:     Entity widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
"""
from os import path
import time

global pysideVers
try:
    from PySide2.QtCore     import *
    from PySide2.QtGui      import *
    from PySide2.QtWidgets  import *
    pysideVers = 2
except:
    from PySide.QtCore      import *
    from PySide.QtGui       import *
    pysideVers = 1

from .iconButton            import IconButton
from .dropDown              import DropDown

class EntityWidget(QWidget):
    """Entity widget display class.

        Args:
            manager (class: `Manager`): The Hestia manager.
            asset (class: `Entity`): The entity to display.
            iconSize (int, optional): Size of the icon to display. Defaults to 64.
            status (int, optional): Status of the button. Defaults to 1.
            parent (class: `QWidget`, optional): Parent widget. Defaults to None.
    """
    def __init__(self, manager=None, mainWindow=None, asset=None, iconSize=64, status=1, parent=None):
        super(EntityWidget, self).__init__(parent=parent)
        self.__manager      = manager
        self.__mainWindow   = mainWindow
        self.__asset        = asset
        
        self.__rootPath = path.dirname(path.abspath(__file__))

        self.__defaultIcon = ""
        if(pysideVers == 2):
            self.__defaultIcon = self.__rootPath + "/../icons/card-image.svg"
        else:
            self.__defaultIcon = self.__rootPath + "/../icons/card-image.png"

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
        self.mainLayout = QVBoxLayout()
        self.groupBox = QGroupBox(self.__name)
        
        self.verticalLayout = QVBoxLayout()
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
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                self.createRightClickMenu(event=event)

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
    
    def createRightClickMenu(self, event):
        """This function invoke a floating menu at mouse position with advanced functionnalities.
        """
        menu = QMenu()

        currentProject = self.__manager.projects[self.__manager.currentProject]
        if(currentProject.categories[currentProject.currentCategory].type == "Assets"):
            # Assign shader to asset button.
            assignShader = menu.addAction("Assign shader to current object")
            assignShader.triggered.connect(self.assignShaderToSelectedAsset)
        elif(currentProject.categories[currentProject.currentCategory].type == "Shots"):
            # Setup scene for shot button.
            setupShot = menu.addAction("Setup shot")
            setupShot.triggered.connect(self.setupSceneForShot)
            # Export to HSHOT button.
            menu.addSeparator()
            extractAssets = menu.addAction("Export to Hestia shot (.hshot)")
            extractAssets.triggered.connect(self.exportShotToHSHOT)

        # Asset management area.
        menu.addSeparator()
        openFileMenu = menu.addAction("Open file")
        openFileMenu.triggered.connect(self.openFile)
        publishEntity = menu.addAction("Publish selection")
        publishEntity.triggered.connect(self.publishSelectionToProjectManager)

        menu.exec_(event.globalPos())
    
    def assignShaderToSelectedAsset(self):
        """Function to assign the shader ID to the selected asset.

        Returns:
            bool: Function status.
        """

        assignStatus = self.__manager.integration.assignShaderToSelectedAsset(version=self.__currentVersion)
        if(assignStatus):
            return True
        else:
            self.__manager.logging.error("Failed to assign shader to selection.")
            return False
        
    def setupSceneForShot(self):
        """Function to setup scene for selected shot.

        Returns:
            bool: Function status.
        """
        currentProject = self.__manager.projects[self.__manager.currentProject]
        
        setupStatus = self.__manager.integration.setupShot(category=currentProject.categories[currentProject.currentCategory],
                                                            shot=self.__asset)

        if(setupStatus):
            return True
        else:
            self.__manager.logging.error("Shot setup failed.")
            return False

    def exportShotToHSHOT(self):
        """Function to export shot to hshot format.

        Returns:
            bool: Function status.
        """
        exportPathDialog = QFileDialog()
        exportPathDialog.setFileMode(QFileDialog.AnyFile)
        exportPathDialog.setNameFilter("Hestia shot (*.hshot *.json)")
        exportPathDialog.setViewMode(QFileDialog.Detail)
        exportPathDialog.setAcceptMode(QFileDialog.AcceptSave)

        if exportPathDialog.exec_():
            exportPath = exportPathDialog.selectedFiles()[0]
        
        print(exportPath)

        self.__manager.integration.extractAssets()
        
        return True
    
    def openFile(self):
        """Function to open file.

        Returns:
            bool: Function status.
        """
        # Show information message.
        warningPopup = QMessageBox.warning(self, self.tr("Hestia"),
                            self.tr("Openning a new file will loose the current datas.\n" + \
                                "Please save before."),
                            QMessageBox.Cancel,
                            QMessageBox.Ok)
        
        if(warningPopup == QMessageBox.Ok):
            self.__currentVersion = self.__versions[self.versionDropDown.currentValue]
            openStatus = self.__manager.integration.openFile(self.__currentVersion)

            if(not openStatus):
                self.__manager.logging.error("Open failed.")

            return openStatus
        else:
            return False

    def publishSelectionToProjectManager(self):
        """Function to publish entity to project manager.

        Returns:
            bool: Function status.
        """
        self.__mainWindow.openPublishWindow(entity=self.__asset)
        return True