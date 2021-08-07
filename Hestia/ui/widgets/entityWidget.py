"""
    :package:   Hestia
    :file:      entityWidget.py
    :brief:     Entity widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
"""
import os

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

from Hestia.core.USD.tools  import USDTools

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
        self._entity        = asset
        
        self.__root_path = os.path.dirname(os.path.abspath(__file__))


        self.__defaultIcon = ""
        if(pysideVers == 2):
            self.__defaultIcon = self.__root_path + "/../icons/card-image.svg"
        else:
            self.__defaultIcon = self.__root_path + "/../icons/card-image.png"

        self.__name           = asset.name
        self.__description    = asset.description
        self.__icon           = asset.preview_file if os.path.isfile(asset.preview_file) else self.__defaultIcon
        self.__iconSize       = iconSize
        self.__versions       = asset.versions
        self.__tasks          = self.getTasks()
        self.__currentTask    = self.__versions[0].task if len(self.__versions) > 0 else None
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

        # Task and verisons layout.
        self.taskAndVersionLayout = QHBoxLayout()

        if(len(self.__versions)>0):
            # Tasks.
            self.taskDropDown = DropDown(
                name="Tasks",
                description="List of tasks available for the asset.",
                datas=self.getTasksNames(),
                defaultValue=0,
                functionToInvoke=self.updateEntity
            )
            self.taskAndVersionLayout.addWidget(self.taskDropDown)

            # Versions.
            self.versionDropDown = DropDown(
                name="Version",
                description="Current version of the asset.",
                datas=self.getVersionsNames(),
                defaultValue=0,
                functionToInvoke=self.updateEntity
            )
            self.taskAndVersionLayout.addWidget(self.versionDropDown)
        else:
            self.noVersionsLabel = QLabel("No versions availables")
            self.taskAndVersionLayout.addWidget(self.noVersionsLabel)

        self.verticalLayout.addLayout(self.taskAndVersionLayout)
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
        
        current_project = self.__manager.get_current_project()

        if(current_project.categories[current_project.current_category].type == "Assets"):
            self.__manager.integration.loadAsset(asset = self._entity,
                                                version = self.__currentVersion)

        elif(current_project.categories[current_project.current_category].type == "Shots"):
            self.__manager.integration.loadShot(asset = self._entity,
                                                version = self.__currentVersion)

        else:
            self.__manager.logging.error("Load failed: not supported type.")
    
    def getTasks(self):
        tasks = []
        for version in self.__versions:
            task = version.task
            if(task not in tasks):
                tasks.append(task)

        return tasks

    def getTasksNames(self):
        """Getting tasks names from version class.

        Returns:
            list:str: Names.
        """
        tasksNames = [task.name for task in self.__tasks]

        if(len(tasksNames) == 0):
            return ["No tasks available."]

        return tasksNames

    def getVersionsNames(self):
        """Getting versions names from version class.

        Returns:
            list:str: Names.
        """
        versionsNames = []
        for version in self.__versions:
            if(version.task == self.__currentTask):
                versionsNames.append("Version %s (%s)" % (version.revision_number, version.type))
        
        if(len(versionsNames) == 0):
            return ["No versions available."]

        return versionsNames

    def updateEntity(self):
        """Update the entity widget with the new selected version.
        """
        if(len(self.__versions) > 0):
            if(self.__currentTask != self.__tasks[self.taskDropDown.currentValue]):
                self.__currentTask = self.__tasks[self.taskDropDown.currentValue]

                self.versionDropDown.datas = self.getVersionsNames()
                self.versionDropDown.currentValue = 0

                self.__currentVersion = [version for version in self.__versions if version.task == self.__currentTask][0]
            else:
                self.__currentVersion = self.__versions[self.versionDropDown.currentValue]

            self.__status = 0 if not self.__currentVersion.type in self.__manager.integration.availableFormats else 1
            self.iconButton.changeButtonStatus(self.__status)
    
    def createRightClickMenu(self, event):
        """This function invoke a floating menu at mouse position with advanced functionnalities.
        """
        menu = QMenu()

        current_project = self.__manager.get_current_project()
        if(current_project.categories[current_project.current_category].type == "Assets"):
            # Assign shader to asset button.
            if(len(self.__versions) > 0):
                pass
        elif(current_project.categories[current_project.current_category].type == "Shots"):
            # Setup scene for shot button.
            setupShot = menu.addAction("Setup shot")
            setupShot.triggered.connect(self.setupSceneForShot)

        # Entity publish area.
        if(self.__manager.get_current_project().support_filetree):
            menu.addSeparator()
            if(len(self.__versions) > 0):
                openFileMenu = menu.addAction("Open file")
                openFileMenu.triggered.connect(self.openFile)
            
            publishEntity = menu.addAction("Publish selection")
            publishEntity.triggered.connect(self.publishSelectionToProjectManager)

        # USD utils.
        if(self.__manager.get_current_project().support_filetree):
            menu.addSeparator()
            if(os.path.isfile(self._entity.path)):
                openFileMenu = menu.addAction("Open with USDView")
                openFileMenu.triggered.connect(lambda state: USDTools.open_usdview(self._entity.path))

        menu.exec_(event.globalPos())
    
    def setupSceneForShot(self):
        """Function to setup scene for selected shot.

        Returns:
            bool: Function status.
        """
        current_project = self.__manager.get_current_project()
        
        # Setup scene.
        setupStatus = self.__manager.integration.setupShot(category=current_project.categories[current_project.current_category],
                                                            shot=self._entity)

        # Import assigned assets.
        assets = [entity for entity in current_project.entities if entity.type == "Assets"]
        for assetID in self._entity.assigned_assets:
            staticAsset = True
            # Get the asset from ID.
            assetToImport = [asset for asset in assets if asset.id == assetID][0]
            
            # Get the last updated version of the asset.
            # TODO: Filter the versions, publish branch need to be merged before to support Version Number.
            self.assetVersions       = assetToImport.versions

            versionToLoad = "Set Dressing"
            if(len([assetRig for assetRig in self.assetVersions if versionToLoad in assetRig.task.name]) == 0):
                versionToLoad = "Rigging"
                staticAsset = False
                if(len([assetRig for assetRig in self.assetVersions if versionToLoad in assetRig.task.name]) == 0):
                    versionToLoad = "Modeling"
                    staticAsset = True
                    if(len([assetRig for assetRig in self.assetVersions if versionToLoad in assetRig.task.name]) == 0):
                        self.currentAssetVersion = None
            
            self.currentAssetVersion = [assetRig for assetRig in self.assetVersions if versionToLoad in assetRig.task.name][0] if len(self.assetVersions) > 0 else None

            if self.currentAssetVersion != None:
                # Import the version inside of the scene.
                self.__manager.integration.loadAsset(asset = assetToImport,
                                                    version = self.currentAssetVersion,
                                                    staticAsset = staticAsset)
            else:
                self.__manager.logging.error("Failed to load %s" % self.assetToImport.name)

        if(setupStatus):
            return True
        else:
            self.__manager.logging.error("Shot setup failed.")
            return False
    
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
        self.__mainWindow.openPublishWindow(entity=self._entity)
        return True