"""
    :package:   Hestia
    :file:      project.py
    :brief:     Project class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

class Project():
    def __init__(self, name="", description=""):
        self.__name         = name
        self.__description  = description

        self.__categories   = []
    
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