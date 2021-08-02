"""
    :package:   Hestia
    :file:      entity.py
    :brief:     Entity base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
from ..links.decorators import sync_entity

from .entity import Entity

class Shot(Entity):
    """Entity class.

    Args:
        versions (list: class: "Version"): Entity's version. Defaults to [].
    """
    def __init__(self, versions=[], *args, **kwargs):
        super(Shot, self).__init__(*args, **kwargs)
        
        self._versions          = versions
        
        self._frame_number      = int(kwargs.get("frame_number", 0))
        self._assigned_assets   = kwargs.get("assigned_assets", [])
    
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

    @property
    @sync_entity
    def frame_number(self):
        """Get the shot duration in frames.

        Returns:
            int: Shot duration.
        """
        return self._frame_number

    @frame_number.setter
    def frame_number(self, new_length):
        """Set the length of the shot.
        
        Args:
            new_length (int): Length (in frames) of the shot.
        """
        self._frame_number = new_length
    
    @property
    @sync_entity
    def assigned_assets(self):
        """Get assets assigned to the shot.

        Returns:
            list: class`Asset`: Assets in shot.
        """
        return self._assigned_assets

    @assigned_assets.setter
    def assigned_assets(self, asset_ids):
        """Set the ids for assets assigned to this shot.
        
        Args:
            asset_ids (list: str): List of assets assigned to this shot.
        """
        self._assigned_assets = asset_ids