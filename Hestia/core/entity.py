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
        id (str): Entity's ID. Defaults to "".
        name (str, optional): Entity's name. Defaults to "".
        description (str, optional): Entity's description. Defaults to "".
        icon (str, optional): Entity's icon. Defaults to "".
        versions (list: class: "Version"): Entity's version. Defaults to [].
    """
    def __init__(self, id = "", name = "", description = "", icon = "", versions=[], **kwargs):
        # Common datas.
        self.__id           = id
        self.__name         = name
        self.__description  = description

        self.__icon         = icon
        self.__versions     = versions
        
        # Shot specific datas.
        self.__frameNumber = 0
        if(kwargs.has_key("frameNumber")):
            self.__frameNbr = kwargs["frameNumber"]

    @property
    def id(self):
        """Get the id of the entity.

        Returns:
            str: Entity's ID.
        """
        return self.__id
    
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
    
    @property
    def versions(self):
        """Get versions of the entity.

        Returns:
            list : Versions of the entity.
        """
        return self.__versions
    
    @versions.setter
    def versions(self, versions):
        """Set versions of the entity.

        Args:
            versions (list): Versions of the entity
        """
        self.__versions = versions
    
    # Shot specific datas.
    @property
    def frameNumber(self):
        """Get the shot duration in frames.

        Returns:
            int: Shot duration.
        """
        return self.__frameNumber