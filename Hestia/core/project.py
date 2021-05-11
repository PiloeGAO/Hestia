"""
    :package:   Hestia
    :file:      project.py
    :brief:     Project class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
"""

import os

class Project():
    """Project class.

    Args:
        id (str, optional): Project's ID. Defaults to "".
        name (str, optional): Project's name. Defaults to "".
        description (str, optional): Project's description. Defaults to "".
    """
    def __init__(self, id="", name="", description="", **kwargs):
        # Project name.
        self.__id           = id
        self.__name         = name
        self.__description  = description

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
        self.__outputFilenameStyle = "lowercase"
        self.__outputFilenameAsset = ""
        self.__outputFilenameShot = ""
        self.__outputFolderPathStyle = "lowercase"
        self.__outputFolderPathAsset = ""
        self.__outputFolderPathShot = ""
        self.__workingFilenameStyle = "lowercase"
        self.__workingFilenameAsset = ""
        self.__workingFilenameShot = ""
        self.__workingFolderPathStyle = "lowercase"
        self.__workingFolderPathAsset = ""
        self.__workingFolderPathShot = ""

        if("mountPoint" in kwargs):
            self.__mountPoint = str(kwargs["mountPoint"])
        if("rootPoint" in kwargs):
            self.__rootPoint = str(kwargs["rootPoint"])
        if("outputFilenameStyle" in kwargs):
            self.__outputFilenameStyle = str(kwargs["outputFilenameStyle"])
        if("outputFilenameAsset" in kwargs):
            self.__outputFilenameAsset = str(kwargs["outputFilenameAsset"])
        if("outputFilenameShot" in kwargs):
            self.__outputFilenameShot = str(kwargs["outputFilenameShot"])
        if("outputFolderPathStyle" in kwargs):
            self.__outputFolderPathStyle = str(kwargs["outputFolderPathStyle"])
        if("outputFolderPathAsset" in kwargs):
            self.__outputFolderPathAsset = str(kwargs["outputFolderPathAsset"])
        if("outputFolderPathShot" in kwargs):
            self.__outputFolderPathShot = str(kwargs["outputFolderPathShot"])
        if("workingFilenameStyle" in kwargs):
            self.__workingFilenameStyle = str(kwargs["workingFilenameStyle"])
        if("workingFilenameAsset" in kwargs):
            self.__workingFilenameAsset = str(kwargs["workingFilenameAsset"])
        if("workingFilenameShot" in kwargs):
            self.__workingFilenameShot = str(kwargs["workingFilenameShot"])
        if("workingFolderPathStyle" in kwargs):
            self.__workingFolderPathStyle = str(kwargs["workingFolderPathStyle"])
        if("workingFolderPathAsset" in kwargs):
            self.__workingFolderPathAsset = str(kwargs["workingFolderPathAsset"])
        if("workingFolderPathShot" in kwargs):
            self.__workingFolderPathShot = str(kwargs["workingFolderPathShot"])
        
        # For debuging, clean this for final branch merge.
        print(self.outputFilenameAsset)
        print(self.outputFolderpathAsset)
        print(self.outputFilenameShot)
        print(self.outputFolderpathShot)
    
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
        return self.__outputFilenameAsset
    
    @property
    def outputFilenameShot(self):
        return self.__outputFilenameShot

    @property
    def outputFolderpathAsset(self):
        return self.__mountPoint + ":" + os.sep + self.__rootPoint + os.sep + self.__outputFolderPathAsset.replace("<Project>", self.__name, 1)
    
    @property
    def outputFolderpathShot(self):
        return self.__mountPoint + ":" + os.sep + self.__rootPoint + os.sep + self.__outputFolderPathShot.replace("<Project>", self.__name, 1)
    
    @property
    def workingFilenameAsset(self):
        return self.__workingFilenameAsset
    
    @property
    def workingFilenameShot(self):
        return self.__workingFilenameShot

    @property
    def workingFolderpathAsset(self):
        return self.__mountPoint + ":" + os.sep + self.__rootPoint + os.sep + self.__workingFolderPathAsset.replace("<Project>", self.__name, 1)
    
    @property
    def workingFolderpathShot(self):
        return self.__mountPoint + ":" + os.sep + self.__rootPoint + os.sep + self.__workingFolderPathShot.replace("<Project>", self.__name, 1)