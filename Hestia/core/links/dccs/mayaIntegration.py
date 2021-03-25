"""
    :package:   Hestia
    :file:      mayaIntegration.py
    :brief:     Maya integration class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os

global integrationActive

try:
    from maya import cmds
except:
    integrationActive = False
else:
    integrationActive = True

from .defaultIntegration import DefaultIntegration

class MayaIntegration(DefaultIntegration):
    """Default integration class.
    """
    def __init__(self, manager=None):
        self.__manager = manager

        if(not integrationActive):
            self.__manager.logging.error("Maya Libraries not found!")

        self._active = integrationActive
        self.initializeFileFormats()

        # Autodesk Maya support instance by using "References". 
        self._supportInstances  = True
        self._instances         = True
    
    def initializeFileFormats(self):
        """Initialize the file formats list.

        Returns:
            list: str: File formats enables.
        """
        self.__manager.logging.info("Initialize File Formats.")
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
            self.__manager.logging.error("Failed to load: " + pluginName)
            pluginActive = False

        return pluginActive
    
    def loadAsset(self, asset=None, version=None):
        """Load the selected asset inside of the scene.

        Returns:
            bool: Status of the import.
        """
        if(not os.path.exists(version.outputPath)):
            self.__manager.logging.error("File not found.")
            return False

        objMatrix = []
        
        if(cmds.attributeQuery("isHestiaAsset", node=cmds.ls(type="transform")[0], exists=True)):
            if(cmds.getAttr(cmds.ls(type="transform")[0] + ".hestiaAssetID") == str(asset.id)
                and cmds.getAttr(cmds.ls(type="transform")[0] + ".hestiaVersionID") == str(version.id)):
                # Saving the previous version matrix.
                objMatrix = cmds.getAttr(cmds.ls(type="transform")[0] + ".matrix")
                # Deleting the previous version.
                cmds.delete(cmds.ls(type="transform")[0])
        
        # Importing the asset and getting the transform node.
        before = set(cmds.ls(type="transform"))

        self.importAsset(version=version)

        after = set(cmds.ls(type="transform"))
        imported = after - before

        cmds.select(imported, r=True)

        # In case of version change, set the new object matrix from the previous one.
        if(objMatrix != []):
            cmds.setAttr(cmds.ls(type="transform")[0] + ".matrix", objMatrix)
        
        # Setting needed attributes for shot assembly.
        cmds.addAttr(attributeType="bool", hidden=1,
                    longName="isHestiaAsset", shortName="isHstAsst")
        cmds.setAttr(cmds.ls(type="transform")[0] + ".isHestiaAsset", 1)

        cmds.addAttr(dataType="string", hidden=1,
                    longName="hestiaAssetID", shortName="hestiaAsstID")
        cmds.setAttr(cmds.ls(type="transform")[0] + ".hestiaAssetID", str(asset.id), type="string")
        
        cmds.addAttr(dataType="string", hidden=1,
                    longName="hestiaVersionID", shortName="hestiaVrsID")
        cmds.setAttr(cmds.ls(type="transform")[0] + ".hestiaVersionID", str(version.id), type="string")

        return True
    
    def loadShot(self, shotPath=""):
        """Load the selected shot inside of the scene.

        Returns:
            bool: Status of the import.
        """
        if(not os.path.exists(shotPath)):
            self.__manager.logging.error("File not found.")
            return False
        
        return NotImplemented
    
    def importAsset(self, version=None):
        """Import the asset inside of Maya.

        Args:
            path (str, optional): Path of the asset. Defaults to "".
        """
        if(self._instances == True and (version.type == ".ma" or version.type == ".mb")):
            cmds.file(version.outputPath, reference=True)
        else:
            cmds.file(version.outputPath, i=True)