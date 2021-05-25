"""
    :package:   Hestia
    :file:      publishWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
    :brief:     Class to create the publish window based on QtWidgets.  
"""
import os
from datetime               import datetime
import shutil
import sys

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

from .core import IOUtils

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
    def __init__(self, manager, mainWindow, entity, parent=None):
        super(PublishWindow, self).__init__(parent=parent)
        self.__manager      = manager
        self.__mainWindow   = mainWindow
        
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
        
        self.outputButtonsLayout = QHBoxLayout()

        self.addOutputButton = QPushButton("Add output")
        self.addOutputButton.clicked.connect(self.addOutput)
        self.outputButtonsLayout.addWidget(self.addOutputButton)

        self.removeOutputButton = QPushButton("Remove last output")
        self.removeOutputButton.clicked.connect(self.removeOutput)
        self.outputButtonsLayout.addWidget(self.removeOutputButton)

        self.mainLayout.addLayout(self.outputButtonsLayout)

        # Preview path.
        self.previewLayout = QHBoxLayout()

        self.previewTitle = QLabel("Preview: None")
        self.previewLayout.addWidget(self.previewTitle)

        self.previewLayout.addStretch()

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
        if(len(self.outputsList) < len(availableFormats)):
            outputChoice = DropDown(name="Export Type", datas=availableFormats)
            self.outputsList.append(outputChoice)
            
            self.outputGrid = GridWidget(manager=self.__manager,
                                        parentGeometry=self.outputScrollArea.geometry(),
                                        xSize=1,
                                        itemList=self.outputsList,
                                        emptyLabel="No outputs in list")
            self.outputScrollArea.setWidget(self.outputGrid)
    
    def removeOutput(self):
        """Remove the last line of the output list.
        """
        if(len(self.outputsList) > 0):
            del self.outputsList[-1]
            
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
        
        self.previewTitle.setText("Preview : %s" % self.__screenshotPath)

    def takeScreenshot(self):
        """Take a screenshot of the scene.
        """
        path = self.__manager.tempFolder + os.sep + "preview.PNG"
        self.__manager.integration.takePlayblast(startFrame=-1, endFrame=-1, path=path)
        self.__screenshotPath = path

        self.previewTitle.setText("Preview : %s" % self.__screenshotPath)
    
    def takePlayblast(self):
        """Take a playblast of the scene.
        """
        if(sys.platform.startswith('win32')):
            format = "avi"
        elif(sys.platform.startswith('darwin')):
            format = "mov"
        else:
            return False
        
        path_raw = self.__manager.tempFolder + os.sep + "preview_raw." + format
        self.__manager.integration.takePlayblast(startFrame=-2, endFrame=0, path=path_raw)

        path = self.__manager.tempFolder + os.sep + "preview.mp4"
        conversionStatus = IOUtils.videoConverter(path_raw, path)
        os.remove(path_raw)

        if(conversionStatus and os.path.isfile(path)):
            self.__screenshotPath = path
            self.previewTitle.setText("Preview : %s" % self.__screenshotPath)
        else:
            self.__manager.logging.error("Conversion failed, aborting.")
        
    def publish(self):
        """Publish function.
        """
        publishTask = self.__entity.tasks[self.taskDropBox.currentValue]
        publishTaskStatus = self.taskStatusDropDown.datas[self.taskStatusDropDown.currentValue]

        publishName = self.publishName.currentValue
        publishComment = self.publishComment.currentValue
        publishVersion = int(self.__currentProject.getLastVersion(entity=self.__entity, taskType=publishTask))
        workingPath = self.__currentProject.getFolderpath(exportType="working", category=self.__category, entity=self.__entity, taskType=publishTask, versionNumber=publishVersion)
        workingFileName = self.__currentProject.getFilename(exportType="working", category=self.__category, entity=self.__entity, taskType=publishTask, versionNumber=publishVersion) + self.__manager.integration.defaultFormat
        outputPath = self.__currentProject.getFolderpath(exportType="output", category=self.__category, entity=self.__entity, taskType=publishTask, versionNumber=publishVersion)
        outputFileNames = []
        previewFilename = self.__currentProject.getFilename(exportType="output", category=self.__category, entity=self.__entity, taskType=publishTask, versionNumber=publishVersion) + "_preview"

        for i, widget in enumerate(self.outputsList):
            outputFileNames.append(self.__currentProject.getFilename(exportType="output", category=self.__category, entity=self.__entity, taskType=publishTask, versionNumber=publishVersion) + self.__manager.integration.availableFormats[widget.currentValue])

        if(publishName != "" and publishComment != ""
            and workingPath != "" and workingFileName != ""
            and outputPath != "" and os.path.isfile(self.__screenshotPath)):
            
            self.hide()
            self.__mainWindow.hide()

            # Create the working and output directories.
            IOUtils.makeFolder(workingPath)
            IOUtils.makeFolder(outputPath)

            # Export files from DCC.
            self.__manager.logging.info("Writing the working file.")
            
            publishWorkingFilePath = workingPath + os.sep + workingFileName
            if(os.path.isfile(publishWorkingFilePath) != True):
                workingSaveStatus = self.__manager.integration.saveFile(workingPath + os.sep + workingFileName)
                if(workingSaveStatus):
                    self.__manager.logging.error("Couldn't save the working file")
            
            publishOutputFilePaths = []
            for i, outputFilename in enumerate(outputFileNames):
                self.__manager.logging.info("Writing output file %s/%s." % (i+1, len(outputFileNames)))
                path = outputPath + os.sep + outputFilename
                if(os.path.isfile(path) != True):
                    extension = os.path.splitext(outputFilename)[1]
                    exportStatus = self.__manager.integration.exportSelection(path=path, extension=extension)

                    # If export failed for current export (example: file already exist),
                    # remove the unnecessary file.
                    if(exportStatus):
                        publishOutputFilePaths.append(path)
                    else:
                        self.__manager.logging.warning("Export failed.")
                else:
                    publishOutputFilePaths.append(path)
            
            # Copy the preview to output folder.
            self.__manager.logging.info("Writing the preview file.")
            IOUtils.copyFile(self.__screenshotPath, outputPath, newName=previewFilename)
            publishPreviewFilePath = outputPath + os.sep + previewFilename + os.path.splitext(self.__screenshotPath)[1]

            self.__manager.logging.info("Publishing online.")
            # Publishing files to the project manager.
            self.__manager.link.publish(
                entity=self.__entity,
                name=publishName,
                comment=publishComment,
                taskTypeID=publishTask.id,
                taskStatus=publishTaskStatus,
                version=publishVersion,
                software=self.__manager.integration.name,
                outputType="", # TODO: Ouput type need to be a list (sometimes ABC and PNG can be published simultaneously)
                workingFilePath=publishWorkingFilePath,
                outputFiles=publishOutputFilePaths,
                previewFilePath=publishPreviewFilePath
            )
            self.__manager.logging.info("Publishing done.")

            # TODO: Find a way to refresh project.
            # Refreshing the project to get last datas uploaded.

            self.__mainWindow.show()

            # Temporary warning message.
            # Show information message.
            QMessageBox.warning(self, self.tr("Hestia"),
                                self.tr("Please close Hestia to get latest updates."),
                                QMessageBox.NoButton,
                                QMessageBox.Ok)

        else:
            # Show information message.
            QMessageBox.warning(self, self.tr("Hestia"),
                                self.tr("Some datas are missing."),
                                QMessageBox.NoButton,
                                QMessageBox.Ok)