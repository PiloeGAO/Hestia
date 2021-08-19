"""
    :package:   Hestia
    :file:      entity.py
    :brief:     Entity base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import os

from Hestia.core.USD.stage import USDStage

from ..links.decorators import sync_entity

class Entity(object):
    """Entity class.

    Args:
        id (str): Entity's ID. Defaults to "".
        name (str, optional): Entity's name. Defaults to "".
        description (str, optional): Entity's description. Defaults to "".
        tasks (list: class: "Task"): Entity's tasks. Defaults to [].
        raw_datas (dict): Raw datas from DB. Defaults to {}.
    """
    def __init__(self, id = "", name = "", description = "", tasks=[], preview_path="", raw_datas={}, is_downloaded=False, *args, **kwargs):
        self._id           = id
        self._name         = name
        self._description  = description
        self._tasks        = tasks
        self._path         = ""
        self._preview_path = preview_path

        self._usd_stage    = USDStage(path=self._path)\
                             if os.path.isfile(self._path)\
                             else None

        self._raw_datas    = raw_datas

        self._is_downloaded = is_downloaded

    @property
    def id(self):
        """Get the id of the entity.

        Returns:
            str: Entity's ID.
        """
        return self._id
    
    @property
    @sync_entity
    def name(self):
        """Get the name of the entity.

        Returns:
            str : The name of the entity.
        """
        return self._name
    
    @name.setter
    def name(self, name):
        """Set the name of the entity.

        Args:
            name (str): The name of the entity
        """
        self._name = name
    
    @property
    @sync_entity
    def description(self):
        """Get the description of the entity.

        Returns:
            str : The description of the entity.
        """
        return self._description
    
    @description.setter
    def description(self, description):
        """Set the description of the entity.

        Args:
            description (str): The description of the entity
        """
        self._description = description

    @property
    @sync_entity
    def tasks(self):
        """Get tasks of the entity.

        Returns:
            list: class:`Task`: Tasks of the entity.
        """
        return self._tasks
    
    @tasks.setter
    def tasks(self, new_tasks):
        """Set tasks of the entity.

        Args:
            new_tasks (list: class`Task`): Tasks of the entity.
        """
        self._tasks = new_tasks
    
    def add_task(self, new_task):
        """Add a task to entity.

        Args:
            new_task (class: `Task`): Task to be added.
        """
        if(new_task in self._tasks):
            raise CoreError("A task can't be added twice to an entity.")
        
        self._tasks.append(new_task)

    @property
    @sync_entity
    def path(self):
        """Get the path to usd main scene.
        
        Returns:
            str: Path.
        """
        # Build USD file if not on the disk.
        if(not self._usd_stage):
            self._usd_stage = USDStage(path=self._path)
            self._usd_stage.create_stage()
        
        return self._path
    
    @path.setter
    def path(self, path):
        """Set the path to usd main scene.
        
        Args:
            path (str): Path
        """
        self._path = path

    @property
    @sync_entity
    def preview_path(self):
        """Get the preview file path.
        
        Returns:
            str: Path
        """
        return self._preview_path

    @preview_path.setter
    def preview_path(self, new_path):
        """Set the preview file path.
        
        Args:
            new_path (str): Path.
        """
        self._preview_path = new_path

    @property
    def is_downloaded(self):
        """Get download status of the entity.
        
        Returns:
            bool: Status
        """
        return self._is_downloaded

    @is_downloaded.setter
    def is_downloaded(self, new_status):
        """Set download status of the entity.
        
        Args:
            new_status (bool): Download status
        """
        self._is_downloaded = new_status
    
    @property
    @sync_entity
    def raw_datas(self):
        """Get the raw datas of the class.

        Returns:
            dict: Raw datas
        """
        return self._raw_datas
    
    @raw_datas.setter
    def raw_datas(self, new_datas):
        """Set the raw datas of the entity.

        Args:
            new_datas (dict): Raw datas
        """
        self._raw_datas = new_datas