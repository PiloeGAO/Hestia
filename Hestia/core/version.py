"""
    :package:   Hestia
    :file:      version.py
    :brief:     Version base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
"""
from os import path

class Version():
    def __init__(self, id="", name="", description="", task=None, workingPath="", outputPath="", type="", revisionNumber=0, **kwargs):
        self.__id               = id
        self.__name             = name
        self.__description      = description
        self.__task             = task
        
        self.__rawDatas = kwargs["rawDatas"] if "rawDatas" in kwargs else ""

        self.__workingPath      = workingPath
        self.__outputPath       = outputPath

        self.__revisionNumber   = revisionNumber
        self.__type = path.splitext(self.__outputPath)[1] if type == "" else type
    
    @property
    def id(self):
        """Get the id of the version.

        Returns:
            str: Version's ID.
        """
        return self.__id
    
    @property
    def name(self):
        """Get the name of the version.

        Returns:
            str : The name of the version.
        """
        if(self.__name == ""):
            return "Revision %s" % self.__revisionNumber
        else:
            return self.__name
    
    @name.setter
    def name(self, name):
        """Set the name of the version.

        Args:
            name (str): The name of the version
        """
        self.__name = name
    
    @property
    def description(self):
        """Get the description of the version.

        Returns:
            str : The description of the version.
        """
        return self.__description
    
    @description.setter
    def description(self, description):
        """Set the description of the version.

        Args:
            description (str): The description of the version
        """
        self.__description = description
    
    @property
    def task(self):
        """Get the task of the version.

        Returns:
            class:`Task`: The task of the version.
        """
        return self.__task
    
    @property
    def rawDatas(self):
        """Get the raw datas of the class.

        Returns:
            dict: Raw datas
        """
        return self.__rawDatas
        
    @property
    def workingPath(self):
        """Get the working path of the version.

        Returns:
            str : The working path of the version.
        """
        return self.__workingPath
    
    @workingPath.setter
    def workingPath(self, workingPath):
        """Set the working path of the version.

        Args:
            workingPath (str): The working path of the version
        """
        self.__workingPath = workingPath
        
    @property
    def outputPath(self):
        """Get the output path of the version.

        Returns:
            str : The output path of the version.
        """
        return self.__outputPath
    
    @outputPath.setter
    def outputPath(self, outputPath):
        """Set the output path of the version.

        Args:
            outputPath (str): The output path of the version
        """
        self.__outputPath = outputPath
        
    @property
    def type(self):
        """Get the output type of the version.

        Returns:
            str : The output type of the version.
        """
        return self.__type
    
    @type.setter
    def type(self, type):
        """Set the output type of the version.

        Args:
            type (str): The output type of the version
        """
        self.__type = type
        
    @property
    def revisionNumber(self):
        """Get the revision number of the version.

        Returns:
            int : The revision number of the version.
        """
        return self.__revisionNumber