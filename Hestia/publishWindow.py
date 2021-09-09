"""
    :package:   Hestia
    :file:      publishWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
    :brief:     Class to create the publish window based on QtWidgets.  
"""
import os
from datetime               import datetime
import sys

from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *

from Hestia.core.manager import current_manager

from Hestia.core.USD import get_usd_extensions
from Hestia.core.USD.stage import USDStage

from .core.IO.path import TemplateManager, FileManager
from .core.IO.encoding import *

from .ui.widgets.iconButton import IconButton
from .ui.widgets.dropDown   import DropDown
from .ui.widgets.lineEdit   import LineEdit
from .ui.widgets.textEdit   import TextEdit
from .ui.widgets.gridWidget import GridWidget

class PublishWindow(QWidget):
    """Publish Window class.

    Args:
        entity (class: `Entity`): Entity to publish.
        parent (class: `QtWidgets`, optional): PyQt parent. Defaults to None.
    """
    def __init__(self, mainWindow, entity, parent=None):
        super(PublishWindow, self).__init__(parent=parent)
        self._manager      = current_manager()
        self._main_window  = mainWindow
        
        self._current_project = self._manager.get_current_project()
        self._category     = self._current_project.categories[self._current_project.current_category]
        self._entity       = entity

        self._workfile_path = ""

        self._screenshot_path = ""
        self._screenshot_support = self._manager.integration.support_screenshots
        
        self._root_path = os.path.dirname(os.path.abspath(__file__))

        self.initUI()

    def initUI(self):
        """Generate the window.
        """

        # Set the window title.
        self.setWindowTitle("Hestia - Publish")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        
        #self.resize(self._windowWidth, self._windowHeight)

        # Set the window style.
        self.setStyle(QStyleFactory.create("Fusion"))

        # Set the main layout component.
        self.mainLayout = QVBoxLayout()

        self.taskLayout = QHBoxLayout()

        # Task drop down.
        self.taskDropBox = DropDown(name="Task", description="Task of the publish.", datas=self.get_tasks_names())
        self.taskLayout.addWidget(self.taskDropBox)

        # Task status drop drown.
        self.taskStatusDropDown = DropDown(name="Status", description="Task status.", datas=["WIP", "WFA"], defaultValue=1)
        self.taskLayout.addWidget(self.taskStatusDropDown)

        self.mainLayout.addLayout(self.taskLayout)

        # Publish name.
        self.publishName = LineEdit(name="Name", description="Publish Name", defaultValue="Publish %s | %s" % (self._entity.name, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        self.mainLayout.addWidget(self.publishName)

        self.mainLayout.setSpacing(0)

        # Publish comment.
        self.publishComment = TextEdit(name="Comment", description="Publish comment.", defaultValue="")
        self.mainLayout.addWidget(self.publishComment)

        # Working file.
        if(self._manager.integration.name == "standalone"):
            self.workLayout = QHBoxLayout()

            self.workTitle = QLabel("Work file: None")
            self.workLayout.addWidget(self.workTitle)

            self.workLayout.addStretch()

            iconPath = self._root_path + "/ui/icons/folder_open_black.svg"
            self.workButton = IconButton(name="Open file browser",description="Locate the workfile",
                                                iconPath=iconPath, iconScale=16,
                                                functionToInvoke=self.openWorkfileExplorer)
            self.workLayout.addWidget(self.workButton)

            self.mainLayout.addLayout(self.workLayout)

        # Output paths.
        self.outputsList = []

        self.outputScrollArea = QScrollArea()
        self.outputGrid = GridWidget(manager=self._manager,
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

        self.export_anim_datas_checkbox = QCheckBox("Export animation datas")
        self.mainLayout.addWidget(self.export_anim_datas_checkbox)

        # Preview path.
        self.previewLayout = QHBoxLayout()

        self.previewTitle = QLabel("Preview: None")
        self.previewLayout.addWidget(self.previewTitle)

        self.previewLayout.addStretch()

        iconPath = self._root_path + "/ui/icons/folder_open_black.svg"
        self.previewButton = IconButton(name="Open file browser",description="Locate the screenshot",
                                            iconPath=iconPath, iconScale=16,
                                            functionToInvoke=self.open_screenshot_explorer)
        self.previewLayout.addWidget(self.previewButton)

        if(self._screenshot_support):
            iconPath = self._root_path + "/ui/icons/photo_camera_black.svg"
            self.screenshotButton = IconButton(name="Take screenshot", description="Take screenshot of current scene.",
                                                iconPath=iconPath, iconScale=16,
                                                status=1, functionToInvoke=self.take_screenshot)
            self.previewLayout.addWidget(self.screenshotButton)
            
            iconPath = self._root_path + "/ui/icons/camera_roll_black.svg"
            self.playblastButton = IconButton(name="Take a video", description="Take video of current scene.",
                                                iconPath=iconPath, iconScale=16,
                                                status=1, functionToInvoke=self.take_playblast)
            self.previewLayout.addWidget(self.playblastButton)

        self.mainLayout.addLayout(self.previewLayout)

        # Publish button.
        self.publishButton = QPushButton("Publish file")
        self.publishButton.clicked.connect(self.publish)
        self.mainLayout.addWidget(self.publishButton)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def get_tasks_names(self):
        """Get all tasks for entity.

        Returns:
            list: str: List of task names.
        """
        return [task.name for task in self._entity.tasks]

    def openWorkfileExplorer(self):
        """Open file explorer to set screenshot path.
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        if dialog.exec_():
            self._workfile_path = dialog.selectedFiles()[0]
        
        self.workTitle.setText("Workfile : %s" % self._workfile_path)

    def addOutput(self):
        """Add a new line in the output list.
        """
        available_formats = [format.upper() for format in self._manager.integration.available_formats]
        if(len(self.outputsList) < len(available_formats)):
            outputChoice = DropDown(name="Export Type", datas=available_formats)
            self.outputsList.append(outputChoice)
            
            self.outputGrid = GridWidget(manager=self._manager,
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
            
            self.outputGrid = GridWidget(manager=self._manager,
                                        parentGeometry=self.outputScrollArea.geometry(),
                                        xSize=1,
                                        itemList=self.outputsList,
                                        emptyLabel="No outputs in list")
            self.outputScrollArea.setWidget(self.outputGrid)

    def open_screenshot_explorer(self):
        """Open file explorer to set screenshot path.
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        if dialog.exec_():
            self._screenshot_path = dialog.selectedFiles()[0]
        
        self.previewTitle.setText("Preview : %s" % self._screenshot_path)

    def take_screenshot(self):
        """Take a screenshot of the scene.
        """
        path = FileManager().temp_directory + os.sep + "preview.PNG"
        self._manager.integration.take_playblast(start_frame=-1, end_frame=-1, path=path)
        self._screenshot_path = path

        self.previewTitle.setText("Preview : %s" % self._screenshot_path)
    
    def take_playblast(self):
        """Take a playblast of the scene.
        """
        if(sys.platform.startswith('win32')):
            format = "avi"
        elif(sys.platform.startswith('darwin')):
            format = "mov"
        else:
            return False
        
        path_raw = FileManager().temp_directory + os.sep + "preview_raw." + format
        self._manager.integration.take_playblast(start_frame=-2, end_frame=0, path=path_raw)

        path = FileManager().temp_directory + os.sep + "preview.mp4"
        conversionStatus = video_converter(path_raw, path)
        os.remove(path_raw)

        if(conversionStatus and os.path.isfile(path)):
            self._screenshot_path = path
            self.previewTitle.setText("Preview : %s" % self._screenshot_path)
        else:
            self._manager.logging.error("Conversion failed, aborting.")
        
    def publish(self):
        """Publish function.
        """
        publish_task = self._entity.tasks[self.taskDropBox.currentValue]
        publish_task_status = self.taskStatusDropDown.datas[self.taskStatusDropDown.currentValue]

        publishName = self.publishName.currentValue
        publishComment = self.publishComment.currentValue
        publishVersion = int(self._entity.get_next_version(task_type=publish_task))
        working_path = TemplateManager().get_folderpath(exportType="working", project=self._current_project, category=self._category, entity=self._entity, task_type=publish_task, version_number=publishVersion)
        workingFileName = TemplateManager().get_filename(exportType="working", project=self._current_project, category=self._category, entity=self._entity, task_type=publish_task, version_number=publishVersion)
        output_path = TemplateManager().get_folderpath(exportType="output", project=self._current_project, category=self._category, entity=self._entity, task_type=publish_task, version_number=publishVersion)
        output_filenames = []
        output_extensions = []
        export_animation_datas = bool(self.export_anim_datas_checkbox.isChecked())
        previewFilename = TemplateManager().get_filename(exportType="output", project=self._current_project, category=self._category, entity=self._entity, task_type=publish_task, version_number=publishVersion) + "_preview"

        for i, widget in enumerate(self.outputsList):
            output_filenames.append(TemplateManager().get_filename(exportType="output", project=self._current_project, category=self._category, entity=self._entity, task_type=publish_task, version_number=publishVersion))
            output_extensions.append(self._manager.integration.available_formats[widget.currentValue])

        if(publishName != "" and publishComment != ""
            and working_path != "" and workingFileName != ""
            and output_path != "" and os.path.isfile(self._screenshot_path)):
            
            self.hide()
            self._main_window.hide()

            # Create the working and output directories.
            FileManager().make_folder(working_path)
            FileManager().make_folder(output_path)

            # Export files from DCC.
            self._manager.logging.info("Writing the working file.")
            
            working_extension = self._manager.integration.default_format
            if(self._manager.integration.name == "standalone"):
                working_extension = os.path.splitext(self._workfile_path)[1][1:]

            publish_working_file_path = working_path + os.sep + workingFileName + "." + working_extension

            if(not os.path.isfile(publish_working_file_path)):
                working_save_status = False

                if(self._manager.integration.name == "standalone"
                    and os.path.isfile(self._workfile_path)):
                    working_save_status = FileManager.copy_file(self._workfile_path, os.path.split(publish_working_file_path)[0], new_name=workingFileName)
                else:
                    working_save_status = self._manager.integration.save_file(publish_working_file_path)
                
                if(not working_save_status):
                    self._manager.logging.error("Couldn't save the working file")
            
            publish_output_file_paths = []
            for i, output_filename in enumerate(output_filenames):
                self._manager.logging.info("Writing output file %s/%s." % (i+1, len(output_filenames)))

                extension = output_extensions[i]
                path = output_path + os.sep + output_filename + "." + extension
                if(not os.path.isfile(path)):
                    export_status = False

                    if(self._manager.integration.name == "standalone"
                        and os.path.isfile(self._workfile_path)):
                        export_status = FileManager.copy_file(self._workfile_path, 
                                                            os.path.split(path)[0],
                                                            new_name=os.path.splitext(output_filename)[0])
                        # TODO: Find a more elegent way to process this.
                        # Auto export should be done if input not match the output (ex: .usd > .usda).
                        path = output_path + os.sep + output_filename + "." + os.path.splitext(self._workfile_path)[1][1:]
                    else:
                        export_status = self._manager.integration.export_selection(path=path, extension=extension.lower(), export_animation_datas=export_animation_datas)

                    # If export failed for current export (example: file already exist),
                    # remove the unnecessary file.
                    if(export_status):
                        publish_output_file_paths.append(path)
                    else:
                        self._manager.logging.warning("Export failed for {}.".format(path))
                else:
                    publish_output_file_paths.append(path)
            
            # Copy the preview to output folder.
            self._manager.logging.info("Writing the preview file.")
            FileManager().copy_file(self._screenshot_path, output_path, new_name=previewFilename)
            publishPreviewFilePath = output_path + os.sep + previewFilename + os.path.splitext(self._screenshot_path)[1]

            self._manager.logging.info("Publishing online.")
            # Publishing files to the project manager.
            publish_status = self._manager.link.publish(
                entity=self._entity,
                name=publishName,
                comment=publishComment,
                task_type_ID=publish_task.id,
                task_status=publish_task_status,
                version=publishVersion,
                software=self._manager.integration.name,
                output_type="", # TODO: Ouput type need to be a list (sometimes ABC and PNG can be published simultaneously)
                working_file_path=publish_working_file_path,
                output_files=publish_output_file_paths,
                preview_file_path=publishPreviewFilePath
            )

            if(publish_status):
                # Link the USD output to master.
                output_files = [file for file in publish_output_file_paths if os.path.splitext(file)[1][1:] in get_usd_extensions()]

                if(len(output_files) > 0):
                    output_file = output_files[0]

                    from pxr import Usd

                    master_stage = Usd.Stage.Open(self._entity.path)

                    path_ref_prim = "/{}".format(publish_task.name).replace(" ", "_")

                    if(len([x for x in master_stage.Traverse() if x.GetPath() == path_ref_prim]) == 0):
                        # Create the prim and add reference to output
                        self._manager.logging.info("Creating the Prim to create the reference.")
                        ref_prim = master_stage.OverridePrim(path_ref_prim)
                    else:
                        # Change the reference to the new ouptut.
                        self._manager.logging.info("Clearing previous references.")
                        ref_prim = master_stage.GetPrimAtPath(path_ref_prim)
                        ref_prim.GetReferences().ClearReferences()

                    self._manager.logging.info("Add the reference to the master stage.")
                    ref_prim.GetReferences().AddReference(output_file)
                    master_stage.GetRootLayer().Save()
                else:
                    self._manager.logging.warning("No USD files in outputs, nothing will be linked to master stage.")

                # Export done log.
                self._manager.logging.info("Publishing done.")
            else:
                self._manager.logging.info("Publishing failed.")

                # Temporary warning message.
                # Show information message.
                QMessageBox.critical(self, self.tr("Hestia"),
                                    self.tr("Publish failed, please contact your TD"),
                                    QMessageBox.NoButton,
                                    QMessageBox.Ok)

            # Refreshing the project to get last datas uploaded.
            self._entity.is_downloaded = False
            self._main_window.refresh()
            self._main_window.show()

        else:
            # Show information message.
            QMessageBox.warning(self, self.tr("Hestia"),
                                self.tr("Some datas are missing."),
                                QMessageBox.NoButton,
                                QMessageBox.Ok)