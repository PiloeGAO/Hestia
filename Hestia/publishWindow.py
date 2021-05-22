"""
    :package:   Hestia
    :file:      publishWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
    :brief:     Class to create the publish window based on QtWidgets.  
"""
from genericpath import isfile
from Hestia.core.project import Project
import os
from datetime               import datetime

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

from .ui.widgets.iconButton import IconButton
from .ui.widgets.dropDown   import DropDown
from .ui.widgets.lineEdit   import LineEdit
from .ui.widgets.textEdit   import TextEdit
from .ui.widgets.gridWidget import GridWidget

class PublishWindow(QWidget):
    """Publish Window class.

    Args:
        manager (class: `Manager`): Manager of Hestia.
        entity (class: `Entity`): Entity to publish.
        parent (class: `QtWidgets`, optional): PyQt parent. Defaults to None.
    """
    def __init__(self, manager, entity, parent=None):
        super(PublishWindow, self).__init__(parent=parent)
        self.__manager      = manager
        
        self.__currentProject = self.__manager.projects[self.__manager.currentProject]
        self.__category     = self.__currentProject.categories[self.__currentProject.currentCategory]
        self.__entity       = entity

        self.__screenshotPath = ""
        self.__screenshotSupport = self.__manager.integration.supportScreenshots
        
        self.__rootPath = os.path.dirname(os.path.abspath(__file__))

        self.initUI()

    def initUI(self):
        """Generate the window.
        """

        # Set the window title.
        self.setWindowTitle("Hestia - Publish")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        
        #self.resize(self.__windowWidth, self.__windowHeight)

        # Set the window style.
        self.setStyle(QStyleFactory.create("Fusion"))

        # Set the main layout component.
        self.mainLayout = QVBoxLayout()

        self.taskLayout = QHBoxLayout()

        # Task drop down.
        self.taskDropBox = DropDown(name="Task", description="Task of the publish.", datas=self.getTasksNames())
        self.taskLayout.addWidget(self.taskDropBox)

        # Task status drop drown.
        self.taskStatusDropDown = DropDown(name="Status", description="Task status.", datas=["WIP", "WFA"], defaultValue=1)
        self.taskLayout.addWidget(self.taskStatusDropDown)

        self.mainLayout.addLayout(self.taskLayout)

        # Publish name.
        self.publishName = LineEdit(name="Name", description="Publish Name", defaultValue="Publish %s | %s" % (self.__entity.name, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        self.mainLayout.addWidget(self.publishName)

        self.mainLayout.setSpacing(0)

        # Publish comment.
        self.publishComment = TextEdit(name="Comment", description="Publish comment.", defaultValue="")
        self.mainLayout.addWidget(self.publishComment)

        # Output paths.
        self.outputsList = []

        self.outputScrollArea = QScrollArea()
        self.outputGrid = GridWidget(manager=self.__manager,
                                    parentGeometry=self.outputScrollArea.geometry(),
                                    xSize=1,
                                    itemList=self.outputsList,
                                    emptyLabel="No outputs in list")
        self.outputScrollArea.setWidget(self.outputGrid)
        self.mainLayout.addWidget(self.outputScrollArea)

        self.addOutputButton = QPushButton("Add output")
        self.addOutputButton.clicked.connect(self.addOutput)
        self.mainLayout.addWidget(self.addOutputButton)

        # Preview path.
        self.previewLayout = QHBoxLayout()

        self.previewTitle = QLabel("Preview: ")
        self.previewLayout.addWidget(self.previewTitle)

        if(pysideVers == 2):
            iconPath = self.__rootPath + "/ui/icons/folder2-open.svg"
        else:
            iconPath = self.__rootPath + "/ui/icons/folder2-open.png"
        self.previewButton = IconButton(name="Open file browser",description="Locate the screenshot",
                                            iconPath=iconPath, iconScale=16,
                                            functionToInvoke=self.openScreenshotExplorer)
        self.previewLayout.addWidget(self.previewButton)

        if(self.__screenshotSupport):
            if(pysideVers == 2):
                iconPath = self.__rootPath + "/ui/icons/camera.svg"
            else:
                iconPath = self.__rootPath + "/ui/icons/camera.png"
            self.screenshotButton = IconButton(name="Take screenshot", description="Take screenshot of current scene.",
                                                iconPath=iconPath, iconScale=16,
                                                status=1, functionToInvoke=self.takeScreenshot)
            self.previewLayout.addWidget(self.screenshotButton)
            
            if(pysideVers == 2):
                iconPath = self.__rootPath + "/ui/icons/camera-reels.svg"
            else:
                iconPath = self.__rootPath + "/ui/icons/camera-reels.png"
            self.playblastButton = IconButton(name="Take a video", description="Take video of current scene.",
                                                iconPath=iconPath, iconScale=16,
                                                status=1, functionToInvoke=self.takePlayblast)
            self.previewLayout.addWidget(self.playblastButton)

        self.mainLayout.addLayout(self.previewLayout)

        # Publish button.
        self.publishButton = QPushButton("Publish file")
        self.publishButton.clicked.connect(self.publish)
        self.mainLayout.addWidget(self.publishButton)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def getTasksNames(self):
        """Get all tasks for entity.

        Returns:
            list: str: List of task names.
        """
        return [task.name for task in self.__entity.tasks]

    def addOutput(self):
        """Add a new line in the output list.
        """
        availableFormats = [format[1:].upper() for format in self.__manager.integration.availableFormats]
        outputChoice = DropDown(name="Export Type", datas=availableFormats)
        self.outputsList.append(outputChoice)
        
        self.outputGrid = GridWidget(manager=self.__manager,
                                    parentGeometry=self.outputScrollArea.geometry(),
                                    xSize=1,
                                    itemList=self.outputsList,
                                    emptyLabel="No outputs in list")
        self.outputScrollArea.setWidget(self.outputGrid)

    def openScreenshotExplorer(self):
        """Open file explorer to set screenshot path.
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        if dialog.exec_():
            self.__screenshotPath = dialog.selectedFiles()[0]

    def takeScreenshot(self):
        """Take a screenshot of the scene.
        """
        # TODO: Implement the screenshot support inside of DCCs.
        self.__screenshotPath = "SCREENSHOT"
        print("Screenshot OK.")
    
    def takePlayblast(self):
        """Take a playblast of the scene.
        """
        # TODO: Implement the screenshot support inside of DCCs.
        self.__screenshotPath = "PLAYBLAST"
        print("Playblast OK.")

    def publish(self):
        """Publish function.
        """
        publishName = self.publishName.currentValue
        publishComment = self.publishComment.currentValue
        workingPath = self.__currentProject.getFolderpath(exportType="working", category=self.__category, entity=self.__entity, taskType=self.__entity.tasks[self.taskDropBox.currentValue], versionNumber=0)
        workingFileName = self.__currentProject.getFilename(exportType="working", category=self.__category, entity=self.__entity, taskType=self.__entity.tasks[self.taskDropBox.currentValue], versionNumber=0) + self.__manager.integration.defaultFormat
        outputPaths = []
        outputFileNames = []

        for i, widget in enumerate(self.outputsList):
            outputPaths.append(self.__currentProject.getFolderpath(exportType="output", category=self.__category, entity=self.__entity, taskType=self.__entity.tasks[self.taskDropBox.currentValue], versionNumber=0))
            outputFileNames.append(self.__currentProject.getFilename(exportType="output", category=self.__category, entity=self.__entity, taskType=self.__entity.tasks[self.taskDropBox.currentValue], versionNumber=0) + self.__manager.integration.availableFormats[widget.currentValue])

        if(publishName != "" and publishComment != ""
            and workingPath != "" and workingFileName != ""
            and len(outputPaths) > 0 and os.path.isfile(self.__screenshotPath)):

            print("Publish Name: %s" % publishName)
            print("Publish Comment: %s" % publishComment)
            print("Working file path: %s" % workingPath)
            print("Working filename: %s" % workingFileName)
            
            for i, outputPath in enumerate(outputPaths):
                print("%i > %s" % (i, outputPath + os.sep + outputFileNames[i]))
            print("Publish preview file: %s" % self.__screenshotPath)
            
            self.hide()
        else:
            # Show information message.
            QMessageBox.warning(self, self.tr("Hestia"),
                                self.tr("Some datas are missing."),
                                QMessageBox.NoButton,
                                QMessageBox.Ok)