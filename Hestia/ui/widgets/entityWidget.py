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
    def __init__(self, manager=None, main_window=None, asset=None, icon_size=64, status=1, parent=None):
        super(EntityWidget, self).__init__(parent=parent)
        self._manager      = manager
        self._main_window  = main_window
        self._entity       = asset
        
        self._root_path = os.path.dirname(os.path.abspath(__file__))


        self._default_icon = ""
        if(pysideVers == 2):
            self._default_icon = self._root_path + "/../icons/card-image.svg"
        else:
            self._default_icon = self._root_path + "/../icons/card-image.png"

        self._name            = asset.name
        self._description     = asset.description
        self._icon            = asset.preview_file if os.path.isfile(asset.preview_file) else self._default_icon
        self._icon_size       = icon_size
        self._versions        = asset.versions
        self._tasks           = self.get_tasks()
        self._current_task    = self._versions[0].task if len(self._versions) > 0 else None
        self._current_version = self._versions[0] if len(self._versions) > 0 else None

        if(len(self._versions) > 0):
            self._status = 0 if not self._current_version.type in self._manager.integration.available_formats else 1
        else:
            self._status = 0

        self.initUI()
    
    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Vertical.
        self.main_layout = QVBoxLayout()

        group_box_title = self._name
        if(self._current_version != None):
            group_box_title += " - Version {} ({})".format(
                self._current_version.revision_number,
                self._current_version.type
            )
        else:
            group_box_title += " - No versions available"

        self.entity_box = QGroupBox(group_box_title)
        
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setContentsMargins(0,0,0,0)

        # Button / Logo.
        self.icon_button = IconButton(self._name, self._description, self._icon, self._icon_size, self._status, self.import_asset)
        self.vertical_layout.addWidget(self.icon_button)

        # Task and verisons layout.
        self.task_and_version_layout = QHBoxLayout()

        if(len(self._versions)>0):
            # Tasks.
            self.task_dropdown = DropDown(
                name="Tasks",
                description="List of tasks available for the asset.",
                datas=self.get_tasks_names(),
                defaultValue=0,
                functionToInvoke=self.update_entity
            )
            self.task_and_version_layout.addWidget(self.task_dropdown)
        else:
            self.no_versions_label = QLabel("No versions availables")
            self.task_and_version_layout.addWidget(self.no_versions_label)

        self.vertical_layout.addLayout(self.task_and_version_layout)
        self.vertical_layout.addStretch(1)

        # Add the main layout to the window.
        self.entity_box.setLayout(self.vertical_layout)
        self.main_layout.addWidget(self.entity_box)
        self.setLayout(self.main_layout)

    def mousePressEvent(self, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                self.createRightClickMenu(event=event)

    def import_asset(self):
        """Function that invoke the import in core.
        """
        self._manager.logging.info("Import %s" % self._name)
        
        current_project = self._manager.get_current_project()

        if(current_project.categories[current_project.current_category].type == "Assets"):
            self._manager.integration.load_asset(asset = self._entity,
                                                version = self._current_version)

        elif(current_project.categories[current_project.current_category].type == "Shots"):
            self._manager.integration.load_shot(asset = self._entity,
                                                version = self._current_version)

        else:
            self._manager.logging.error("Load failed: not supported type.")
    
    def get_tasks(self):
        tasks = []
        for version in self._versions:
            task = version.task
            if(task not in tasks):
                tasks.append(task)

        return tasks

    def get_tasks_names(self):
        """Getting tasks names from version class.

        Returns:
            list:str: Names.
        """
        tasks_names = [task.name for task in self._tasks]

        if(len(tasks_names) == 0):
            return ["No tasks available."]

        return tasks_names

    def update_entity(self, version=None):
        """Update the entity widget with the new selected version.
        """
        if(not version):
            if(self._current_task != self._tasks[self.task_dropdown.currentValue]):
                self._current_task = self._tasks[self.task_dropdown.currentValue]
                version = [version for version in self._versions if version.task == self._current_task][0]

        self._current_version = version

        self._status = 0 if not self._current_version.type in self._manager.integration.available_formats else 1
        self.icon_button.changeButtonStatus(self._status)

        self.entity_box.setTitle("{} - Version {} ({})".format(self._name, version.revision_number, version.type))

    def createRightClickMenu(self, event):
        """This function invoke a floating menu at mouse position with advanced functionnalities.
        """
        menu = QMenu()

        if(len(self._versions) > 0):
            version_menu = menu.addMenu("Versions: ")
            # Only get versions for current task.
            versions_for_task = [version for version in self._versions if version.task == self._current_task]
            for current_version in versions_for_task:
                version_menu.addAction(
                    "Version {} ({})".format(current_version.revision_number, current_version.type),
                    (lambda version=current_version: self.update_entity(version=version))
                )
        else:
            menu.addAction("No versions available.")

        current_project = self._manager.get_current_project()
        if(current_project.categories[current_project.current_category].type == "Shots"):
            # Setup scene for shot button.
            menu_setup_shot = menu.addAction("Setup shot")
            menu_setup_shot.triggered.connect(self.setup_scene_for_shot)

        # Entity publish area.
        if(self._manager.get_current_project().support_filetree
            and self._current_version != None):
            menu.addSeparator()
            if(len(self._versions) > 0):
                menu_open_file = menu.addAction("Open file")
                menu_open_file.triggered.connect(self.open_file)
            
            menu_publish_entity = menu.addAction("Publish selection")
            menu_publish_entity.triggered.connect(self.publish_selection_to_pm)

        # USD utils.
        if(self._manager.get_current_project().support_filetree
            and self._current_version != None):
            menu.addSeparator()
            if(os.path.splitext(self._entity.path)[1] in [".usda", ".usd"]
                and os.path.isfile(self._entity.path)):
                menu_open_file_usdview_master = menu.addAction("Open with master stage in USDView")
                menu_open_file_usdview_master.triggered.connect(lambda state: USDTools.open_usdview(self._entity.path))

        menu.exec_(event.globalPos())
    
    def setup_scene_for_shot(self):
        """Function to setup scene for selected shot.
        TODO: Move the content of this to core.

        Returns:
            bool: Function status.
        """
        current_project = self._manager.get_current_project()
        
        # Setup scene.
        setup_status = self._manager.integration.setup_shot(category=current_project.categories[current_project.current_category],
                                                            shot=self._entity)

        # Import assigned assets.
        assets = [entity for entity in current_project.entities if entity.type == "Assets"]
        for asset_ID in self._entity.assigned_assets:
            static_asset = True
            # Get the asset from ID.
            asset_to_import = [asset for asset in assets if asset.id == asset_ID][0]
            
            # Get the last updated version of the asset.
            # TODO: Filter the versions, publish branch need to be merged before to support Version Number.
            self.asset_versions       = asset_to_import.versions

            version_to_load = "Set Dressing"
            if(len([asset for asset in self.asset_versions if version_to_load in asset.task.name]) == 0):
                version_to_load = "Rigging"
                static_asset = False
                if(len([asset for asset in self.asset_versions if version_to_load in asset.task.name]) == 0):
                    version_to_load = "Modeling"
                    static_asset = True
                    if(len([asset for asset in self.asset_versions if version_to_load in asset.task.name]) == 0):
                        self.current_asset_version = None
            
            self.current_asset_version = [asset for asset in self.asset_versions if version_to_load in asset.task.name][0] if len(self.asset_versions) > 0 else None

            if self.current_asset_version != None:
                # Import the version inside of the scene.
                self._manager.integration.load_asset(asset = asset_to_import,
                                                    version = self.current_asset_version,
                                                    static_asset = static_asset)
            else:
                self._manager.logging.error("Failed to load %s" % self.asset_to_import.name)

        if(setup_status):
            return True
        else:
            self._manager.logging.error("Shot setup failed.")
            return False
    
    def open_file(self):
        """Function to open file.

        Returns:
            bool: Function status.
        """
        # Show information message.
        warning_popup = QMessageBox.warning(self, self.tr("Hestia"),
                            self.tr("Openning a new file will loose the current datas.\n" + \
                                "Please save before."),
                            QMessageBox.Cancel,
                            QMessageBox.Ok)
        
        if(warning_popup == QMessageBox.Ok):
            open_status = self._manager.integration.open_file(self._current_version)

            if(not open_status):
                self._manager.logging.error("Open failed.")

            return open_status
        else:
            return False

    def publish_selection_to_pm(self):
        """Function to publish entity to project manager.

        Returns:
            bool: Function status.
        """
        self._main_window.openPublishWindow(entity=self._entity)
        return True