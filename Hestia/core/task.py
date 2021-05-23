"""
    :package:   Hestia
    :file:      task.py
    :brief:     Task base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
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

        self.__rawDatas = kwargs["rawDatas"] if "rawDatas" in kwargs else ""
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
    
    @property
    def type(self):
        """Get the type of the class.

        Returns:
            str: Task type.
        """
        return self.__type
    
    @property
    def rawDatas(self):
        """Get the raw datas of the class.

        Returns:
            dict: Raw datas
        """
        return self.__rawDatas