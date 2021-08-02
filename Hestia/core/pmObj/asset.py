"""
    :package:   Hestia
    :file:      entity.py
    :brief:     Entity base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
from ..links.decorators import sync_entity

from .entity import Entity

class Asset(Entity):
    """Asset class.

    Args:
        versions (list: class: "Version"): Entity's version. Defaults to [].
    """
    def __init__(self, versions=[], *args, **kwargs):
        super(Asset, self).__init__(*args, **kwargs)
        
        self._versions = versions
    
    @property
    @sync_entity
    def versions(self):
        """Get versions of the asset.

        Returns:
            list: class:`Version` : Versions of the asset.
        """
        return self._versions
    
    @versions.setter
    def versions(self, versions):
        """Set versions of the asset.

        Args:
            versions (list: class:`Version`): Versions of the asset.
        """
        self._versions = versions

    def get_next_version(self, task_type):
        """Find the next version for publishing

        Args:
            entity (class: `Entity`): Entity.
            task_type (class: `Task`): Task.

        Returns:
            int: Version number.
        """
        version_number = 0
        for version in self._versions:
            if(version.task.id == task_type.id and version.revision_number > version_number):
                version_number = version.revision_number
        version_number = version_number + 1

        return version_number