"""
    :package:   Hestia
    :file:      entity.py
    :brief:     Entity base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

class Entity():
    """Entity class.

    Args:
        name (str, optional): Entity's name. Defaults to "".
        description (str, optional): Entity's description. Defaults to "".
        path (str, optional): Entity's path. Defaults to "".
        icon (str, optional): Entity's icon. Defaults to "".
        parent (class: "Entity", optional): Entity's parent. Defaults to None.
    """
    def __init__(self, name = "", description = "", path = "", icon = "", parent = None):
        self.__parent       = parent
        self.__type         = "entity"

        self.__name         = name
        self.__description  = description

        self.__path         = path
        self.__icon         = icon
    
    @property
    def parent(self):
        """Get the parent of the entity.

        Returns:
            class: "Entity" : The parent of the entity.
        """
        return self.__parent
    
    @parent.setter
    def parent(self, parent):
        """Set the parent of the entity.

        Args:
            parent (class: "Entity"): The parent of the entity
        """
        self.__parent = parent
    
    @property
    def name(self):
        """Get the name of the entity.

        Returns:
            str : The name of the entity.
        """
        return self.__name
    
    @name.setter
    def name(self, name):
        """Set the name of the entity.

        Args:
            name (str): The name of the entity
        """
        self.__name = name
    
    @property
    def description(self):
        """Get the description of the entity.

        Returns:
            str : The description of the entity.
        """
        return self.__description
    
    @description.setter
    def description(self, description):
        """Set the description of the entity.

        Args:
            description (str): The description of the entity
        """
        self.__description = description
    
    @property
    def path(self):
        """Get the path of the entity.

        Returns:
            str : The path of the entity.
        """
        return self.__path
    
    @path.setter
    def path(self, path):
        """Set the path of the entity.

        Args:
            path (str): The path of the entity
        """
        self.__path = path
    
    @property
    def icon(self):
        """Get the icon of the entity.

        Returns:
            str : The icon of the entity.
        """
        return self.__icon
    
    @icon.setter
    def icon(self, icon):
        """Set the icon of the entity.

        Args:
            icon (str): The icon of the entity
        """
        self.__icon = icon