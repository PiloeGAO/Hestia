"""
    :package:   Hestia
    :file:      defaultIntegration.py
    :brief:     Default integration class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""

class DefaultIntegration(object):
    """Default integration class.
    """
    def __init__(self, manager=None):
        self._manager = manager
        
        self._name = "standalone"

        self._active = False

        self._defaultFormat = ""
        self._availableFormats = ["usda"]

        self._supportScreenshots = False
    
    @property
    def name(self):
        """Get the name of the integration.

        Returns:
            str: Integration name
        """
        return self._name

    @property
    def defaultFormat(self):
        """Get the default format.

        Returns:
            str: Default format/extension.
        """
        return self._defaultFormat

    @property
    def availableFormats(self):
        """Get the available formats.

        Returns:
            list: str: Formats usable by the dccs.
        """
        return self._availableFormats
    
    @property
    def supportScreenshots(self):
        """Get the screenshots support.

        Returns:
            bool: Is screenshot support is available.
        """
        return self._supportScreenshots
    
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
    
    def loadAsset(self, asset=None, version=None):
        """Load the selected asset inside of the scene.

        Args:
            asset (class:"Entity"): Asset datas. Defaults to None.
            version (class:"Version"): Version datas. Defaults to None.

        Returns:
            bool: load status.
        """
        return NotImplemented
    
    def setupShot(self, category=None, shot=None):
        """Setup shot values (eg: Framerate, duration, camera...) inside of the scene.

        Args:
            category (class: "Category"): Categrory datas. Defaults to None.
            shot (class: "Entity"): Shot datas. Defaults to None.

        Returns:
            bool: Setup status.
        """
        return NotImplemented
    
    def loadShot(self, asset=None, version=None):
        """Load the selected shot inside of the scene.

        Args:
            asset (class:"Entity"): Asset datas. Defaults to None.
            version (class:"Version"): Version datas. Defaults to None.

        Returns:
            bool: load status.
        """
        return NotImplemented
    
    def buildShot(self, shotPath = ""):
        """Build the shot from shot assembly system.

        Args:
            shotPath (str): Shot path. Defaults to "".

        Args:
            shotPath (str, optional): [description]. Defaults to "".
        """
        return NotImplemented
    
    def takePlayblast(self, start_frame, endFrame, path):
        """Take a playblast of the scene.

        Args:
            start_frame (int): Start frame.
            endFrame (int): End frame.
            path (sty): Ouput path.

        Returns:
            bool: Function status.
        """
        return NotImplementedError

    def openFile(self, path):
        """Open the file in the DCC.

        Args:
            path (str): File path.

        Returns:
            bool: Function status.
        """
        return NotImplementedError

    def saveFile(self, path):
        """Save current file to the given path.

        Args:
            path (str): File path.

        Returns:
            bool: Functions status.
        """
        return NotImplementedError

    def exportSelection(self, path, extension):
        """Export selection to the path with the correct format.

        Args:
            path (str): Output path.
            extension (str): Extensionof the file.

        Returns:
            bool: Function status.
        """
        return NotImplementedError