"""
    :package:   Hestia
    :file:      entity.py
    :brief:     Entity base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
"""

class Entity():
    """Entity class.

    Args:
        manager (class: "Manager"): The Hestia Manager.
        entityType (str): Entity's type. Defaults to "Assets".
        id (str): Entity's ID. Defaults to "".
        name (str, optional): Entity's name. Defaults to "".
        description (str, optional): Entity's description. Defaults to "".
        icon (str, optional): Entity's icon. Defaults to "".
        tasks (list: class: "Task"): Entity's tasks. Defaults to [].
        versions (list: class: "Version"): Entity's version. Defaults to [].
    """
    def __init__(self, manager, entityType = "Assets", id = "", name = "", description = "", icon = "", tasks=[], versions=[], **kwargs):
        self.__manager      = manager
        # Common datas.
        self.__type         = entityType
        self.__id           = id
        self.__name         = name
        self.__description  = description

        self.__iconDownloaded = False
        self.__icon         = icon
        self.__tasks        = tasks
        self.__versions     = versions
        
        # Shot specific datas.
        self.__frameNumber = int(kwargs["frameNumber"]) if "frameNumber" in kwargs else 0

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
        # Download the preview if not local.
        if(not self.__iconDownloaded):
            self.__icon = self.__manager.link.downloadPreview(entityType=self.__type, entityId=self.__id)
            self.__iconDownloaded = True
        
        return self.__icon
    
    @icon.setter
    def icon(self, icon):
        """Set the icon of the entity.

        Args:
            icon (str): The icon of the entity
        """
        self.__icon = icon
        self.__iconDownloaded = True
    
    @property
    def tasks(self):
        """Get tasks of the entity.

        Returns:
            list: class:`Task`: Task of the entity.
        """
        return self.__tasks
    
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