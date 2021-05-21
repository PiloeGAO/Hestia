"""
    :package:   Hestia
    :file:      project.py
    :brief:     Project class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.3
"""

from Hestia.core.version import Version
from Hestia.core.task import Task
from Hestia.core.category import Category
from Hestia.core.entity import Entity
import os

class Project():
    """Project class.

    Args:
        id (str, optional): Project's ID. Defaults to "".
        name (str, optional): Project's name. Defaults to "".
        description (str, optional): Project's description. Defaults to "".
    """
    def __init__(self, id="", name="", description="", tasks=[], **kwargs):
        # Project name.
        self.__id           = id
        self.__name         = name
        self.__description  = description
        self.__tasks        = tasks

        # Project technical datas.
        self.__framerate = int(float(kwargs["fps"])) if "fps" in kwargs else 0
        self.__ratio = kwargs["ratio"] if "ratio" in kwargs else ""
        self.__resolution = int(kwargs["resolution"]) if "resolution" in kwargs else 1080
        self.__startFrame = int(kwargs["startFrame"]) if "startFrame" in kwargs else 1000
        self.__preRoll = int(kwargs["preRoll"]) if "preRoll" in kwargs else 24
        self.__postRoll = int(kwargs["postRoll"]) if "postRoll" in kwargs else 24

        # Project categories.
        self.__categories   = []
        self.__currentCategory = 0

        # Project file management.
        self.__mountPoint = str(kwargs["mountPoint"]) if "mountPoint" in kwargs else ""
        self.__rootPoint = str(kwargs["rootPoint"]) if "rootPoint" in kwargs else ""
        self.__outputFilenameAsset = str(kwargs["outputFilenameAsset"]) if "outputFilenameAsset" in kwargs else ""
        self.__outputFilenameShot = str(kwargs["outputFilenameShot"]) if "outputFilenameShot" in kwargs else ""
        self.__outputFolderPathAsset = str(kwargs["outputFolderPathAsset"]) if "outputFolderPathAsset" in kwargs else ""
        self.__outputFolderPathShot = str(kwargs["outputFolderPathShot"]) if "outputFolderPathShot" in kwargs else ""
        self.__workingFilenameAsset = str(kwargs["workingFilenameAsset"]) if "workingFilenameAsset" in kwargs else ""
        self.__workingFilenameShot = str(kwargs["workingFilenameShot"]) if "workingFilenameShot" in kwargs else ""
        self.__workingFolderPathAsset = str(kwargs["workingFolderPathAsset"]) if "workingFolderPathAsset" in kwargs else ""
        self.__workingFolderPathShot = str(kwargs["workingFolderPathShot"]) if "workingFolderPathShot" in kwargs else ""
    
    @property
    def id(self):
        """Get the id of the project.

        Returns:
            str: Project's ID.
        """
        return self.__id

    @property
    def name(self):
        """Get the name of the project.

        Returns:
            str: Project's name.
        """
        return self.__name

    @name.setter
    def name(self, name):
        """Set the name fo the project.

        Args:
            name (str): Project's name.
        """
        self.__name = name
    
    @property
    def description(self):
        """Get the description of the project.

        Returns:
            str: Project's description.
        """
        return self.__description

    @description.setter
    def description(self, description):
        """Set the description fo the project.

        Args:
            description (str): Project's description.
        """
        self.__description = description
    
    @property
    def tasks(self):
        """Get the tasks of the projects.

        Returns:
            list(class:`Task`): Tasks.
        """
        return self.__tasks
    
    @tasks.setter
    def tasks(self, tasks):
        """Set the tasks of the project.

        Args:
            tasks (list: class:`Tasks`): New tasks.
        """
        self.__tasks = tasks
    
    def addTask(self, newTask):
        """Add a task to project.

        Args:
            newTask (class: "Task"): New task to add.
        """
        self.__tasks.append(newTask)
    
    @property
    def framerate(self):
        """Get the framerate of the project.

        Returns:
            str: Project's framerate.
        """
        return self.__framerate
    
    @property
    def ratio(self):
        """Get the ratio of the project.

        Returns:
            str: Project's ratio.
        """
        return self.__ratio

    @property
    def resolution(self):
        """Get the resolution of the project.

        Returns:
            str: Project's resoltuion.
        """
        # TODO: Build a resolution manager with ratio selection.
        return 1920, 1080
    
    @property
    def startFrame(self):
        """Get the start frame value of the project.

        Returns:
            int: Frame number.
        """
        return self.__startFrame

    @property
    def preRoll(self):
        """Get the pre-roll value of the project.

        Returns:
            int: Frame number.
        """
        return self.__preRoll
    
    @property
    def postRoll(self):
        """Get the post-roll value of the project.

        Returns:
           int: Frame number
        """
        return self.__postRoll

    @property
    def categories(self):
        """Get the categories of the project.

        Returns:
            list: Project's categories.
        """
        return self.__categories
    
    @categories.setter
    def categories(self, categories):
        """Set the categories of the project.

        Args:
            categories (list): Project's categories.
        """
        self.__categories = categories
    
    @property
    def currentCategory(self):
        """Get the current category of the project.

        Returns:
            int: Category ID.
        """
        return self.__currentCategory
    
    @currentCategory.setter
    def currentCategory(self, id):
        """Set the current category of the project.

        Args:
            id (int): Category ID.
        """
        if(id > 0 and id < len(self.__categories)):
            self.__currentCategory = id
    
    def addCategory(self, newCategory):
        """Add a category to project.

        Args:
            newCategory (class: "Category"): New category to add.
        """
        self.__categories.append(newCategory)
    
    @property
    def outputFilenameAsset(self):
        """Get the filename structure (output only) for assets.

        Returns:
            str: Output filename for assets.
        """
        return self.__outputFilenameAsset
    
    @property
    def outputFilenameShot(self):
        """Get the filename structure (output only) for shots.

        Returns:
            str: Output filename for shots.
        """
        return self.__outputFilenameShot

    @property
    def outputFolderpathAsset(self):
        """Get the folder path structure (output only) for assets.

        Returns:
            str: Output folder path for assets.
        """
        return self.__mountPoint + self.__rootPoint + os.sep + self.__outputFolderPathAsset.replace("<Project>", self.__name, 1)
    
    @property
    def outputFolderpathShot(self):
        """Get the folder path structure (output only) for shots.

        Returns:
            str: Output folder path for shot.
        """
        return self.__mountPoint + self.__rootPoint + os.sep + self.__outputFolderPathShot.replace("<Project>", self.__name, 1)
    
    @property
    def workingFilenameAsset(self):
        """Get the filename structure (working files only) for assets.

        Returns:
            str: Output filename for assets.
        """
        return self.__workingFilenameAsset
    
    @property
    def workingFilenameShot(self):
        """Get the filename structure (working files only) for assets.

        Returns:
            str: Output filename for shots.
        """
        return self.__workingFilenameShot

    @property
    def workingFolderpathAsset(self):
        """Get the folder path structure (working files only) for assets.

        Returns:
            str: Output folder path for assets.
        """
        return self.__mountPoint + self.__rootPoint + os.sep + self.__workingFolderPathAsset.replace("<Project>", self.__name, 1)
    
    @property
    def workingFolderpathShot(self):
        """Get the folder path structure (working files only) for shots.

        Returns:
            str: Output folder path for shots.
        """
        return self.__mountPoint + self.__rootPoint + os.sep + self.__workingFolderPathShot.replace("<Project>", self.__name, 1)
    
    def getFolderpath(self, exportType="output", category=None, entity=None, taskType=None, versionNumber=0):
        """Get the folderpath for entity.

        Args:
            exportType (str, optional): Export type, "output" ou "working". Defaults to "output".
            category (class:`Category`, optional): Category of the entity. Defaults to None.
            entity (class:`Entity`, optional): Entity. Defaults to None.
            taskType (class:`Task`, optional): Task. Defaults to None.
            versionNumber (int, optional): Version of the entity, use "-1" for autocount. Defaults to 0.

        Returns:
            str: Folder path.
        """
        path = ""

        if(versionNumber == -1):
            # Find the last version number automaticly.
            versionNumber = 1
            for version in entity.versions:
                if(version.task.id == taskType.id and version.revisionNumber > versionNumber):
                    versionNumber = version.revisionNumber
            versionNumber = versionNumber + 1

        if(exportType == "output"):
            if(category.type == "Assets"):
                path = self.outputFolderpathAsset
                path = path.replace("<AssetType>", category.name, 1)
                path = path.replace("<Asset>", entity.name, 1)
            else:
                path = self.outputFolderpathShot
                path = path.replace("<Sequence>", category.name, 1)
                path = path.replace("<Shot>", entity.name, 1)
        elif(exportType == "working"):
            if(category.type == "Assets"):
                path = self.workingFolderpathAsset
                path = path.replace("<AssetType>", category.name, 1)
                path = path.replace("<Asset>", entity.name, 1)
            else:
                path = self.workingFolderpathShot
                path = path.replace("<Sequence>", category.name, 1)
                path = path.replace("<Shot>", entity.name, 1)
        else:
            return "./%s_%s_<TaskType>_<Version>/"
        
        path = path.replace("<TaskType>", taskType.name.lower().replace(" ", ""), 1)
        path = path.replace("<Version>", "V%03d" % versionNumber)

        return path

    def getFilename(self, exportType="output", category=None, entity=None, taskType=None, versionNumber=0):
        """Get the filename for the entity.

        Args:
            exportType (str, optional): Export type, "output" ou "working". Defaults to "output".
            category (class:`Category`, optional): Category of the entity. Defaults to None.
            entity (class:`Entity`, optional): Entity. Defaults to None.
            taskType (class:`Task`, optional): Task. Defaults to None.
            versionNumber (int, optional): Version of the entity, use "-1" for autocount. Defaults to 0.

        Returns:
            str: File name.
        """
        filename = ""

        if(versionNumber == -1):
            # Find the last version number automaticly.
            versionNumber = 1
            for version in entity.versions:
                if(version.task.id == taskType.id and version.revisionNumber > versionNumber):
                    versionNumber = version.revisionNumber
            versionNumber = versionNumber + 1

        if(exportType == "output"):
            if(category.type == "Assets"):
                filename = self.outputFilenameAsset
                filename = filename.replace("<AssetType>", category.name, 1)
                filename = filename.replace("<Asset>", entity.name, 1)
            else:
                filename = self.outputFilenameShot
                filename = filename.replace("<Sequence>", category.name, 1)
                filename = filename.replace("<Shot>", entity.name, 1)
        elif(exportType == "working"):
            if(category.type == "Assets"):
                filename = self.workingFilenameAsset
                filename = filename.replace("<AssetType>", category.name, 1)
                filename = filename.replace("<Asset>", entity.name, 1)
            else:
                filename = self.outputFilenameShot
                filename = filename.replace("<Sequence>", category.name, 1)
                filename = filename.replace("<Shot>", entity.name, 1)
        else:
            return "%s_%s_<TaskType>_<Version>" % (category.name, entity.name)
        
        filename = filename.replace("<TaskType>", taskType.name.lower().replace(" ", "_"), 1)
        filename = filename.replace("<Version>", "V%03d" % versionNumber)

        return filename

    @property
    def entities(self):
        """Get all entities stored in the project.

        Returns:
            list:`class:Entity`: Entities from the project.
        """
        # TODO: Move to comprehensive list.
        entities = []
        if(len(self.categories) > 0):
            for category in self.__categories:
                for entity in category.entities:
                    entities.append(entity)
        return entities
