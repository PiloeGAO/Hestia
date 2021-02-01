"""
    :package:   Hestia
    :file:      project.py
    :brief:     Project class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

import os

class Project():
    def __init__(self, name = "", path = "", onlineDatas = [], entities = []):
        self.__name         = name

        if(os.path.isdir(path)):
            self.__path         = path
            self.__type         = 0

            self.generateEntitiesFromFolderTree(path)
        else:
            self.__type         = 1

            self.generateEntitiesFromOnline(onlineDatas)

        self.__types        = ["folder", "online"]

        self.__entities     = entities
    
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
        self.__name == name
    
    @property
    def entities(self):
        """Get the entities stored in the project.

        Returns:
            list(class: "Entity"): Entities.
        """
        return self.__entities
    
    def generateEntitiesFromFolderTree(self, path):
        """Generate entities from a folder path.

        Args:
            path (str): Folder path.

        Returns:
            class: "NotImplementedError": Method not implemented.
        """
        return NotImplementedError
    
    def generateEntitiesFromOnline(self, onlineDatas):
        """Generate entities from online datas.

        Args:
            onlineDatas (list): Data fetched from online server.

        Returns:
            class: "NotImplementedError": Method not implemented.
        """
        return NotImplementedError