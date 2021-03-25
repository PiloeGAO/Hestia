"""
    :package:   Hestia
    :file:      defaultIntegration.py
    :brief:     Default integration class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

class DefaultIntegration(object):
    """Default integration class.
    """
    def __init__(self, manager=None):
        self.__manager = manager
        
        self._active = False

        self._availableFormats = []

        self._supportInstances = False
        self._instances = False
    
    @property
    def availableFormats(self):
        """Get the available formats.

        Returns:
            list: str: Formats usable by the dccs.
        """
        return self._availableFormats
    
    @property
    def supportInstances(self):
        """Get the instance support.

        Returns:
            bool: Is instance available in the current dcc.
        """
        return self._supportInstances
    
    @property
    def instances(self):
        """Get the instance import status.

        Returns:
            bool: Is asset should be imported as instance.
        """
        return self._instances
    
    @instances.setter
    def instances(self, newStatus):
        """Set the instance import status.

        Args:
            newStatus (bool): New status.
        """
        print("Instances new status" + str(newStatus))
        self._instances = newStatus
    
    def initializeFileFormats(self):
        """Initialize the file formats list.

        Returns:
            list: str: File formats enables.
        """
        return NotImplemented
    
    def loadExternalPlugin(self):
        """Load external plugins needed by the implementation (exemple: for special formats...)

        Returns:
            bool: Status of the loading.
        """
        return NotImplemented
    
    def loadAsset(self, assetPath=""):
        """Load the selected asset inside of the scene.

        Returns:
            bool: Status of the import.
        """
        return NotImplemented
    
    def loadShot(self, shotPath=""):
        """Load the selected shot inside of the scene.

        Returns:
            bool: Status of the import.
        """
        return NotImplemented
    
    
    def importAsset(self, path = ""):
        """Import the asset inside of default.

        Args:
            path (str, optional): Path of the asset. Defaults to "".
        """
        return NotImplemented