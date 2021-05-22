"""
    :package:   Hestia
    :file:      guerillaIntegration.py
    :brief:     Guerilla Render integration class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.3
"""
import os

global integrationActive

try:
    import guerilla
except:
    integrationActive = False
else:
    integrationActive = True

from .defaultIntegration import DefaultIntegration

class GuerillaIntegration(DefaultIntegration):
    """Default integration class.
    """
    def __init__(self, manager=None):
        self.__manager = manager

        self._name = "Guerilla"

        if(not integrationActive):
            self.__manager.logging.error("Guerilla Libraries not found!")

        self._active = integrationActive
        self.initializeFileFormats()

        # Guerilla Render support instance by using "References". 
        self._supportInstances  = True
        self._instances         = True
    
    def initializeFileFormats(self):
        """Initialize the file formats list.

        Returns:
            list: str: File formats enables.
        """
        self.__manager.logging.info("Initialize File Formats.")
        self._availableFormats = [".gproject", ".abc"]

        pluginFormats = {}
        for plugin in pluginFormats:
            for subPlugin in pluginFormats[plugin]:
                loadPluginStatus = self.loadExternalPlugin(pluginName=subPlugin)
                if(loadPluginStatus is not True):
                    break

            if(loadPluginStatus):
                self._availableFormats.append(plugin)
    
    def loadExternalPlugin(self, pluginName):
        """Load external plugins needed by the implementation (exemple: for special formats...)

        Returns:
            bool: Status of the loading.
        """
        return True
    
    def loadAsset(self, asset=None, version=None):
        """Load the selected asset inside of the scene.

        Args:
            asset (class:"Entity"): Asset datas. Defaults to None.
            version (class:"Version"): Version datas. Defaults to None.

        Returns:
            bool: load status.
        """
        if(not os.path.exists(version.outputPath)):
            self.__manager.logging.error("File not found.")
            return False

        return NotImplemented
    
    def loadShot(self, asset=None, version=None):
        """Load the selected shot inside of the scene.

        Args:
            asset (class:"Entity"): Asset datas. Defaults to None.
            version (class:"Version"): Version datas. Defaults to None.

        Returns:
            bool: load status.
        """
        if(not os.path.exists(version.outputPath)):
            self.__manager.logging.error("File not found.")
            return False

        if(version.type == ".gproject"):
            return NotImplemented

        elif(version.type == ".hshot"):
            # HSHOT format is a JSON file.
            # Invoke build mechanic.
            self.buildShot(shotPath=version.ouputPath)
            return False
        else:
            return False
    
    def buildShot(self, shotPath = ""):
        """Build the shot from shot assembly system.

        Args:
            shotPath (str): Shot path. Defaults to "".

        Args:
            shotPath (str, optional): [description]. Defaults to "".
        """
        if(not os.path.exists(shotPath)):
            self.__manager.logging.error("File not found.")
            return False
        
        return NotImplemented
    
    def importAsset(self, asset=None, version=None):
        """Import the asset inside of Guerilla.

        Args:
            path (str, optional): Path of the asset. Defaults to "".
        """
        if(self.isInstanceImport(version=version)):
            return NotImplemented
        else:
            return NotImplemented
    
    def isInstanceImport(self, version=None):
        """Return the status for instance import.

        Returns:
            bool: Instance status.
        """
        if(self._instances == True and (version.type == ".gproject")):
            return True
        else:
            return False
    
    def assignShaderToSelectedAsset(self, version):
        """Assign a shader ID to an Hestia asset.

        Args:
            version (class:"Version"): Version datas. Defaults to None.

        Returns:
            bool: Function status.
        """
        return NotImplemented

    def extractAssets(self):
        """Extracts assets for shot building file.
        """
        return NotImplemented