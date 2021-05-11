"""
    :package:   Hestia
    :file:      task.py
    :brief:     Task base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
"""

class Task():
    """Task class.

    Args:
        entityType (str): Entity's type. Defaults to "Assets".
        id (str): Entity's ID. Defaults to "".
        name (str, optional): Entity's name. Defaults to "".
        description (str, optional): Entity's description. Defaults to "".
    """
    def __init__(self, taskType = "Assets", id = "", name = "", **kwargs):
        # Common datas.
        self.__type         = taskType
        self.__id           = id
        self.__name         = name

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
    def type(self):
        """Get the type of the class.

        Returns:
            str: Task type.
        """
        return self.__type