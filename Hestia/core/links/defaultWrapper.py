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
        self._manager       = manager

        self._current_user  = User(username=getpass.getuser() + "(Local Mode)")
        self._active        = False

        self._users         = []
    
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

        Returns:
            NotImplementedError: Projects not implemented.
        """
        raise CoreError("Not implemented in the default wrapper.")
    
    def get_datas_from_project(self, project):
        """Get data for the selected project.

        Args:
            project (str): Project datas.

        Returns:
            NotImplementedError: Projects not implemented.
        """
        raise CoreError("Not implemented in the default wrapper.")

    def convert_templates(self, raw_datas={}):
        """Convert templates for project path management to Hestia.
        
        Args:
            raw_datas (dict): Data from project request.
        
        Returns:
            dict: Path templates
        """
        raise CoreError("Not implemented in the default wrapper.")