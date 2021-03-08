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
    
    def loadAsset(self, asset=None, version=None):
        """Load the selected asset inside of the scene.

        Returns:
            bool: Status of the import.
        """
        if(not os.path.exists(version.outputPath)):
            logging.error("File not found.")
            return False

        # Importing the asset and getting the transform node.
        before = set(cmds.ls(type="transform"))
        cmds.file(version.outputPath, i=True)
        after = set(cmds.ls(type="transform"))
        imported = after - before

        #cmds.select(clear=True)
        cmds.select(imported, r=True)
        
        # Setting needed attributes for shot assembly.
        cmds.addAttr(attributeType="bool", hidden=1,
                    longName="isHestiaAsset", shortName="isHstAsst")
        cmds.setAttr(cmds.ls(type="transform")[0] + ".isHestiaAsset", 1)

        cmds.addAttr(dataType="string", hidden=1,
                    longName="hestiaAssetID", shortName="hestiaAsstID")
        cmds.setAttr(cmds.ls(type="transform")[0] + ".assetID", str(asset.id), type="string")
        
        cmds.addAttr(dataType="string", hidden=1,
                    longName="hestiaVersionID", shortName="hestiaVrsID")
        cmds.setAttr(cmds.ls(type="transform")[0] + ".versionID", str(version.id), type="string")

        
        
        return True
    
    def loadShot(self, shotPath=""):
        """Load the selected shot inside of the scene.

        Returns:
            bool: Status of the import.
        """
        if(not os.path.exists(shotPath)):
            logging.error("File not found.")
            return False
        
        return NotImplemented