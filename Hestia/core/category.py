"""
    :package:   Hestia
    :file:      category.py
    :brief:     Category base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

class Category():
    def __init__(self, name="", description="", type=""):
        self.__name             = name
        self.__description      = description
        self.__type             = type

        self.__entities         = []

    @property
    def name(self):
        """Get the name of the category.

        Returns:
            str: Category's name.
        """
        return self.__name

    @name.setter
    def name(self, name):
        """Set the name fo the category.

        Args:
            name (str): Category's name.
        """
        self.__name = name
    
    @property
    def description(self):
        """Get the description of the category.

        Returns:
            str: Category's description.
        """
        return self.__description

    @description.setter
    def description(self, description):
        """Set the description of the category.

        Args:
            description (str): Category's description.
        """
        self.__description = description
    
    @property
    def type(self):
        """Get the type of the category.

        Returns:
            str: Category's type.
        """
        return self.__type
    
    @property
    def entities(self):
        """Get the entities stored in the category.

        Returns:
            list: Category's entities.
        """
        return self.__entities
    
    @entities.setter
    def entities(self, entities):
        """Set the entities of the category.

        Args:
            entities (list): Category's entities.
        """
        self.__entities = entities
    
    def addEntity(self, entity):
        """Add an entity to the category.

        Args:
            entity (class: "Entity"): New entity to add.
        """
        self.__entities.append(entity)