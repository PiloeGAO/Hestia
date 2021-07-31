"""
    :package:   Hestia
    :file:      project.py
    :brief:     Project class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import os

from .entity import Entity

from ..IO.path import *

class Project(Entity):
    """Project class.
    """
    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

        # Project technical datas.
        self._framerate         = float(kwargs.get("fps", 0))
        self._ratio             = kwargs.get("ratio", "")
        self._resolution        = int(kwargs.get("resolution", 1080))
        self._start_frame       = int(kwargs.get("start_frame", 1000))
        self._pre_roll          = int(kwargs.get("pre_roll", 24))
        self._post_roll         = int(kwargs.get("_post_roll", 24))

        # Project team.
        self._team = []

        # Project categories.
        self._categories        = []
        self._current_category  = 0

        # Path manager
        self._paths_template    = kwargs.get("paths_template", {})
        self._support_filetree  = True if self._paths_template != {} else False

    @property
    def framerate(self):
        """Get the framerate of the project.

        Returns:
            str: Project's framerate.
        """
        return self._framerate
    
    @property
    def ratio(self):
        """Get the ratio of the project.

        Returns:
            str: Project's ratio.
        """
        return self._ratio

    @property
    def resolution(self):
        """Get the resolution of the project.

        Returns:
            str: Project's resoltuion.
        """
        # TODO: Build a resolution manager with ratio selection.
        return 1920, 1080
    
    @property
    def start_frame(self):
        """Get the start frame value of the project.

        Returns:
            int: Frame number.
        """
        return self._start_frame

    @property
    def pre_roll(self):
        """Get the pre-roll value of the project.

        Returns:
            int: Frame number.
        """
        return self._pre_roll
    
    @property
    def post_roll(self):
        """Get the post-roll value of the project.

        Returns:
           int: Frame number
        """
        return self._post_roll

    @property
    def categories(self):
        """Get the categories of the project.

        Returns:
            list: Project's categories.
        """
        return self._categories
    
    @categories.setter
    def categories(self, categories):
        """Set the categories of the project.

        Args:
            categories (list): Project's categories.
        """
        self._categories = categories
    
    @property
    def current_category(self):
        """Get the current category of the project.

        Returns:
            int: Category ID.
        """
        return self._current_category
    
    @current_category.setter
    def current_category(self, id):
        """Set the current category of the project.

        Args:
            id (int): Category ID.
        """
        if(id >= 0 and id < len(self._categories)):
            self._current_category = id
    
    def add_category(self, new_category):
        """Add a category to project.

        Args:
            new_category (class: "Category"): New category to add.
        """
        self._categories.append(new_category)
    
    @property
    def team(self):
        """Get the team working on the project.

        Returns:
            list: class:`User`: Team members.
        """
        return self._team

    @team.setter
    def team(self, new_team):
        """Set the team working on the project.

        Args:
            new_team (list: class:`User`): Team members.
        """
        self._team = new_team

    def add_team_member(self, user):
        """Add a member to the team.

        Args:
            user (class:`User`): User to add to the team.
        """
        self._team.append(user)
    
    @property
    def entities(self):
        """Get all entities stored in the project.

        Returns:
            list:`class:Entity`: Entities from the project.
        """
        # TODO: Move to comprehensive list.
        entities = []
        if(len(self.categories) > 0):
            for category in self._categories:
                for entity in category.entities:
                    entities.append(entity)
        return entities

    @property
    def support_filetree(self):
        """Get filetree support status.

        Returns:
            bool: Filetree support status.
        """
        return self._support_filetree

    @property
    def paths_template(self):
        """Get the template path for current project.
        
        Returns:
            dict: Template.
        
        Raises:
            CoreError: Template path not supported.
        """
        if(not self._support_filetree):
            raise CoreError("Current project doesn't support path management.")

        return self._paths_template