"""
    :package:   Hestia
    :file:      category.py
    :brief:     Category base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
from ..links.decorators import sync_entity

from .entity import Entity

class Category(Entity):
    """Category class.
    """
    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        
        self._type = kwargs.get("type", "Asset")
        self._entities = []
    
    @property
    def type(self):
        """Get the type of the category.

        Returns:
            str: Category type.
        """
        return self._type

    @property
    @sync_entity
    def entities(self):
        """Get the entities stored in the category.

        Returns:
            list: Category's entities.
        """
        return self._entities
    
    @entities.setter
    def entities(self, entities):
        """Set the entities of the category.

        Args:
            entities (list): Category's entities.
        """
        self._entities = entities
    
    def add_entity(self, entity):
        """Add an entity to the category.

        Args:
            entity (class: "Entity"): New entity to add.
        """
        self._entities.append(entity)