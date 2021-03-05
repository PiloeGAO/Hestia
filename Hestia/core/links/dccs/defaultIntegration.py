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
    def __init__(self):
        self._active = False

        self._availableFormats = []
    
    @property
    def availableFormats(self):
        """Get the available formats.

        Returns:
            list: str: Formats usable by the dccs.
        """
        return self._availableFormats
    
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