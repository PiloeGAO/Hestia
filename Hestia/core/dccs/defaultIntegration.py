"""
    :package:   Hestia
    :file:      defaultIntegration.py
    :brief:     Default integration class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import os

from Hestia.core.USD.tools import USDTools

from Hestia.core.logger                    import get_logging
logger = get_logging(__name__)

class DefaultIntegration(object):
    """Default integration class.
    """
    def __init__(self, manager=None):
        self._manager = manager
        
        self._name = "standalone"

        self._active = False

        self._default_format = "usda"
        self._available_formats = ["usda"]

        self._support_screenshots = False
    
    @property
    def name(self):
        """Get the name of the integration.

        Returns:
            str: Integration name
        """
        return self._name

    @property
    def default_format(self):
        """Get the default format.

        Returns:
            str: Default format/extension.
        """
        return self._default_format

    @property
    def available_formats(self):
        """Get the available formats.

        Returns:
            list: str: Formats usable by the dccs.
        """
        return self._available_formats
    
    @property
    def supportScreenshots(self):
        """Get the screenshots support.

        Returns:
            bool: Is screenshot support is available.
        """
        return self._support_screenshots
    
    def initialize_plugins(self, plugins={}):
        """Initialize the file formats list.

        Returns:
            list: str: File formats enables.
        """
        return NotImplemented
    
    def load_asset(self, asset=None, version=None):
        """Load the selected asset inside of the scene.

        Args:
            asset (class:"Entity"): Asset datas. Defaults to None.
            version (class:"Version"): Version datas. Defaults to None.

        Returns:
            bool: load status.
        """
        return NotImplemented
    
    def setup_shot(self, category=None, shot=None):
        """Setup shot values (eg: Framerate, duration, camera...) inside of the scene.

        Args:
            category (class: "Category"): Categrory datas. Defaults to None.
            shot (class: "Entity"): Shot datas. Defaults to None.

        Returns:
            bool: Setup status.
        """
        return NotImplemented
    
    def load_shot(self, asset=None, version=None):
        """Load the selected shot inside of the scene.

        Args:
            asset (class:"Entity"): Asset datas. Defaults to None.
            version (class:"Version"): Version datas. Defaults to None.

        Returns:
            bool: load status.
        """
        return NotImplemented
    
    def build_shot(self, shotPath = ""):
        """Build the shot from shot assembly system.

        Args:
            shotPath (str): Shot path. Defaults to "".

        Args:
            shotPath (str, optional): [description]. Defaults to "".
        """
        return NotImplemented
    
    def take_playblast(self, start_frame, endFrame, path):
        """Take a playblast of the scene.

        Args:
            start_frame (int): Start frame.
            endFrame (int): End frame.
            path (sty): Ouput path.

        Returns:
            bool: Function status.
        """
        return NotImplementedError

    def open_file(self, version):
        """Open the file in the DCC.

        Args:
            version (class:`Version`): Version of the asset.

        Returns:
            bool: Function status.
        """
        path = version.working_path
        if(os.path.isfile(path)
            and os.path.splitext(path)[1][1:] == self._default_format):
            USDTools.open_usdview(path)
            return True
        else:
            logger.error("Open \"{}\" failed.".format(path))
            return False

    def save_file(self, path):
        """Save current file to the given path.

        Args:
            path (str): File path.

        Returns:
            bool: Functions status.
        """
        return NotImplementedError

    def export_selection(self, path, extension):
        """Export selection to the path with the correct format.

        Args:
            path (str): Output path.
            extension (str): Extensionof the file.

        Returns:
            bool: Function status.
        """
        return NotImplementedError