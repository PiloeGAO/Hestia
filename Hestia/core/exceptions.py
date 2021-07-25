"""
    :package:   Hestia
    :file:      exceptions.py
    :brief:     Exceptions classes.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""

class Error(Exception):
    """Base class for exception in Hestia."""
    pass

class CoreError(Error):
    def __init__(self, message):
        """Exception raised for errors in the core submodule.

        Args:
            message (str): Error message.
        """
        self.message = message

class AppError(Error):
    def __init__(self, message):
        """Exception raised for errors in the app submodule.

        Args:
            message (str): Error message.
        """
        self.message = message