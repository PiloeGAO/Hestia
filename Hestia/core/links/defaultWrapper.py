"""
    :package:   Hestia
    :file:      defaultWrapper.py
    :brief:     Default wrapper class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import getpass

from ..pmObj.user import User

from ..exceptions import CoreError

class DefaultWrapper(object):
    """Default wrapper class.

    Args:
        manager (class: `Manager`): The Hestia Manager.
    """
    def __init__(self, manager=None):
        self._manager = manager

        self._name = "DEFAULT"

        self._current_user = User(username=getpass.getuser() + "(Local Mode)", is_downloaded=True)
        self._active = False

        self._users = []

    @property
    def name(self):
        """Name of the current link used.

        Returns:
            str: Link name.
        """
        return self._name
    
    @property
    def connected(self):
        """Check if the current wrapper is connected.

        Returns:
            bool: Connection status.
        """
        return self._active
    
    @property
    def username(self):
        """get the username of the connected user.

        Returns:
            str: Username.
        """
        return self._current_user.username
    
    def get_open_projects(self):
        """Get open project.
        
        Raises:
            CoreError: Not implemented in default wrapper.
        """
        raise CoreError("Not implemented in the default wrapper.")
    
    def get_datas_from_project(self, raw_datas):
        """Get data for the selected project.

        Args:
            raw_datas (str): Project datas.
        
        Raises:
            CoreError: Not implemented in default wrapper.
        """
        raise CoreError("Not implemented in the default wrapper.")

    def get_datas_for_asset(self, asset):
        """Get data for the given asset.
        
        Args:
            asset (class:`Asset`): Asset to dowload.
        
        Raises:
            CoreError: Not implemented in default wrapper.
        """
        raise CoreError("Not implemented in the default wrapper.")

    def get_datas_for_category(self, category):
        """Get data for the given category.
        
        Args:
            category (class:`Category`): Category to download.
        
        Raises:
            CoreError: Not implemented in default wrapper.
        """
        raise CoreError("Not implemented in the default wrapper.")

    def get_datas_for_shot(self, shot):
        """Get data for the given shot.
        
        Args:
            shot (class:`Shot`): Shot to download.
        
        Raises:
            CoreError: Not implemented in default wrapper.
        """
        raise CoreError("Not implemented in the default wrapper.")

    def get_datas_for_task(self, task):
        """Get data for the given task.
        
        Args:
            task (class:`Task`): Task to download.
        
        Raises:
            CoreError: Not implemented in default wrapper.
        """
        raise CoreError("Not implemented in the default wrapper.")

    def get_datas_for_version(self, version):
        """Get data for the given version.
        
        Args:
            version (class:`Version`): Version to download.
        
        Raises:
            CoreError: Not implemented in default wrapper.
        """
        raise CoreError("Not implemented in the default wrapper.")

    def convert_templates(self, raw_datas={}):
        """Convert templates for project path management to Hestia.
        
        Args:
            raw_datas (dict): Data from project request.
        
        Raises:
            CoreError: Not implemented in default wrapper.
        """
        raise CoreError("Not implemented in the default wrapper.")

    def publish(self, *args, **kwargs):
        """Publish files (working and outputs) to project management system.
        
        Raises:
            CoreError: Not implemented in default wrapper.
        """
        raise CoreError("Not implemented in the default wrapper.")