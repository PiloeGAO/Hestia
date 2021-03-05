"""
    :package:   Hestia
    :file:      mayaIntegration.py
    :brief:     Maya integration class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import logging, os

try:
    from maya import cmds
except:
    logging.error("Maya Libraries not found!")
else:
    global integrationActive
    integrationActive = True

from .defaultIntegration import DefaultIntegration

class MayaIntegration(DefaultIntegration):
    """Default integration class.
    """
    def __init__(self):
        self._active = integrationActive
        self.initializeFileFormats()
    
    def initializeFileFormats(self):
        """Initialize the file formats list.

        Returns:
            list: str: File formats enables.
        """
        logging.info("Initialize File Formats.")
        self._availableFormats = [".ma", ".mb"]

        pluginFormats = {".obj": ["objExport.mll"], ".abc": ["AbcExport.mll", "AbcImport.mll"]}
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
        try:
            cmds.loadPlugin(pluginName)
            pluginActive = True
        except RuntimeError:
            logging.error("Failed to load: " + pluginName)
            pluginActive = False

        return pluginActive
    
    def loadAsset(self, assetPath=""):
        """Load the selected asset inside of the scene.

        Returns:
            bool: Status of the import.
        """
        if(not os.path.exists(assetPath)):
            return False
        
        cmds.file(assetPath, i=True)
        
        return True