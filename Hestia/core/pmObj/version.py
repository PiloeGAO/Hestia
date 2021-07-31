"""
    :package:   Hestia
    :file:      version.py
    :brief:     Version base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
from os import path

from .entity import Entity

class Version(Entity):
    """Version class.

    Args:
        task (class:`Task`, optional): Task assigned to this version. Defaults to None.
        working_path (str, optional): Path to working file. Defaults to "".
        output_path (str, optional): Path to output file. Defaults to "".
        type (str, optional): Output filetype. Defaults to "".
        revision_number (int, optional): Current version number. Defaults to 0.
    """
    def __init__(self, task=None, working_path="", output_path="", type="", revision_number=0, *args, **kwargs):
        super(Version, self).__init__(*args, **kwargs)
        self._task             = task

        self._working_path     = working_path
        self._output_path      = output_path

        self._revision_number  = revision_number
        self._type = path.splitext(self._output_path)[1] if type == "" else type
    
    @property
    def task(self):
        """Get the task of the version.

        Returns:
            class:`Task`: The task of the version.
        """
        return self._task
        
    @property
    def working_path(self):
        """Get the working path of the version.

        Returns:
            str : The working path of the version.
        """
        return self._working_path
    
    @working_path.setter
    def working_path(self, working_path):
        """Set the working path of the version.

        Args:
            working_path (str): The working path of the version
        """
        self._working_path = working_path
        
    @property
    def output_path(self):
        """Get the output path of the version.

        Returns:
            str : The output path of the version.
        """
        return self._output_path
    
    @output_path.setter
    def output_path(self, output_path):
        """Set the output path of the version.

        Args:
            output_path (str): The output path of the version
        """
        self._output_path = output_path
        
    @property
    def type(self):
        """Get the output type of the version.

        Returns:
            str : The output type of the version.
        """
        return self._type
    
    @type.setter
    def type(self, type):
        """Set the output type of the version.

        Args:
            type (str): The output type of the version
        """
        self._type = type
        
    @property
    def revision_number(self):
        """Get the revision number of the version.

        Returns:
            int : The revision number of the version.
        """
        return self._revision_number