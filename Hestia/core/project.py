"""
    :package:   Hestia
    :file:      project.py
    :brief:     Project class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
"""

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
        self.__framerate = 0
        self.__ratio = "16:9"
        self.__resolution = 1080
        self.__startFrame = 1000
        self.__preRoll = 24
        self.__postRoll = 24

        if("fps" in kwargs):
            self.__framerate    = int(float(kwargs["fps"]))
        if("ratio" in kwargs):
            self.__ratio        = kwargs["ratio"]
        if("resolution" in kwargs):
            self.__resolution   = int(kwargs["resolution"])
        if("startFrame" in kwargs):
            self.__startFrame   = int(kwargs["startFrame"])
        if("preRoll" in kwargs):
            self.__preRoll      = int(kwargs["preRoll"])
        if("postRoll" in kwargs):
            self.__postRoll     = int(kwargs["postRoll"])

        # Project categories.
        self.__categories   = []
        self.__currentCategory = 0

        # Project file management.
        self.__mountPoint = ""
        self.__rootPoint = ""
        self.__outputFilenameAsset = ""
        self.__outputFilenameShot = ""
        self.__outputFolderPathAsset = ""
        self.__outputFolderPathShot = ""
        self.__workingFilenameAsset = ""
        self.__workingFilenameShot = ""
        self.__workingFolderPathAsset = ""
        self.__workingFolderPathShot = ""

        if("mountPoint" in kwargs):
            self.__mountPoint = str(kwargs["mountPoint"])
        if("rootPoint" in kwargs):
            self.__rootPoint = str(kwargs["rootPoint"])
        if("outputFilenameAsset" in kwargs):
            self.__outputFilenameAsset = str(kwargs["outputFilenameAsset"])
        if("outputFilenameShot" in kwargs):
            self.__outputFilenameShot = str(kwargs["outputFilenameShot"])
        if("outputFolderPathAsset" in kwargs):
            self.__outputFolderPathAsset = str(kwargs["outputFolderPathAsset"])
        if("outputFolderPathShot" in kwargs):
            self.__outputFolderPathShot = str(kwargs["outputFolderPathShot"])
        if("workingFilenameAsset" in kwargs):
            self.__workingFilenameAsset = str(kwargs["workingFilenameAsset"])
        if("workingFilenameShot" in kwargs):
            self.__workingFilenameShot = str(kwargs["workingFilenameShot"])
        if("workingFolderPathAsset" in kwargs):
            self.__workingFolderPathAsset = str(kwargs["workingFolderPathAsset"])
        if("workingFolderPathShot" in kwargs):
            self.__workingFolderPathShot = str(kwargs["workingFolderPathShot"])
        
        # For debuging, clean this for final branch merge.
        print(self.outputFilenameAsset)
        print(self.outputFolderpathAsset)
        print(self.outputFilenameShot)
        print(self.outputFolderpathShot)

        demoCategory = Category(id="0514641", name="SEQ01", type="Shots")
        demoEntity = Entity(manager=None, entityType="Shots", id="53405140", name="SH0100")
        print(self.getFolderpath(exportType="output", category=demoCategory, taskType="layout", versionNumber=5, shot=demoEntity))
    
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
        return self.__mountPoint + ":" + os.sep + self.__rootPoint + os.sep + self.__outputFolderPathAsset.replace("<Project>", self.__name, 1)
    
    @property
    def outputFolderpathShot(self):
        """Get the folder path structure (output only) for shots.

        Returns:
            str: Output folder path for shot.
        """
        return self.__mountPoint + ":" + os.sep + self.__rootPoint + os.sep + self.__outputFolderPathShot.replace("<Project>", self.__name, 1)
    
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
        return self.__mountPoint + ":" + os.sep + self.__rootPoint + os.sep + self.__workingFolderPathAsset.replace("<Project>", self.__name, 1)
    
    @property
    def workingFolderpathShot(self):
        """Get the folder path structure (working files only) for shots.

        Returns:
            str: Output folder path for shots.
        """
        return self.__mountPoint + ":" + os.sep + self.__rootPoint + os.sep + self.__workingFolderPathShot.replace("<Project>", self.__name, 1)
    
    def getFolderpath(self, exportType="output", category=None, taskType="", versionNumber=0, **kwargs):
        """Get the folderpath.

        Args:
            exportType (str, optional): Export type, output or working. Defaults to "output".
            entityType (str, optional): Entity type, Assets or Shots. Defaults to "Assets".
            entity (class: `Entity`): Entity.
            taskType (str, optional): Task name. Defaults to "".
            versionNumber (int, optional): Version number, use -1 for auto count. Defaults to 0.

        Returns:
            str: Path generated.
        """
        path = ""

        if(exportType == "output"):
            if(category.type == "Assets"):
                path = self.outputFolderpathAsset
                path = path.replace("<Type>", category.name, 1)
                path = path.replace("<Asset>", kwargs["asset"].name, 1)
            else:
                path = self.outputFolderpathShot
                path = path.replace("<Sequence>", category.name, 1)
                path = path.replace("<Shot>", kwargs["shot"].name, 1)
        elif(exportType == "working"):
            if(category.type == "Assets"):
                path = self.workingFolderpathAsset
                path = path.replace("<Type>", category.name, 1)
                path = path.replace("<Asset>", kwargs["asset"].name, 1)
            else:
                path = self.workingFolderpathShot
                path = path.replace("<Sequence>", category.name, 1)
                path = path.replace("<Shot>", kwargs["shot"].name, 1)
        else:
            return "./"
        
        path = path.replace("<TaskType>", taskType)
        path = path.replace("<Version>", "V%03d" % versionNumber)

        return path

    def getFilename():
        pass