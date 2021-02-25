"""
    :package:   Hestia
    :file:      defaultWrapper.py
    :brief:     Default wrapper class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import getpass

from ..project   import Project
from ..category  import Category
from ..entity    import Entity

class DefaultWrapper(object):
    def __init__(self):
        self._username = getpass.getuser() + "(Local Mode)"
    
    @property
    def username(self):
        """get the username of the connected user.

        Returns:
            str: Username.
        """
        return self._username
    
    def getOpenProjects(self):
        """Get open project.

        Returns:
            NotImplementedError: Projects not implemented.
        """
        return NotImplementedError
    
    def getDatasFromProject(self, project):
        """Get data for the selected project.

        Args:
            project (str): Project datas.

        Returns:
            NotImplementedError: Projects not implemented.
        """
        return NotImplementedError