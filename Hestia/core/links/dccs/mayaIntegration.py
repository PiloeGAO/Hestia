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

        Args:
            asset (class:"Entity"): Asset datas. Defaults to None.
            version (class:"Version"): Version datas. Defaults to None.

        Returns:
            bool: load status.
        """
        if(not os.path.exists(version.outputPath)):
            self.__manager.logging.error("File not found.")
            return False
        
        # Importing the asset and getting the transform node.
        before = set(cmds.ls(type="transform"))

        self.importAsset(version=version)

        after = set(cmds.ls(type="transform"))
        imported = after - before

        # Create a group that will contain asset except for instances.
        if(not self.isInstanceImport(version=version)):
            groupName = asset.name

            if(cmds.objExists(groupName)):
                groupName = groupName + "_bis"

            cmds.group(imported, n=groupName)
            cmds.select(groupName, r=True)
        else:
            cmds.select(imported, r=True)
        
        currentAsset = cmds.ls(sl=True)[0]

        # Setting needed attributes for shot assembly.
        cmds.addAttr(attributeType="bool", hidden=0,
                    longName="isHestiaAsset", shortName="isHstAsst")
        cmds.setAttr(currentAsset + ".isHestiaAsset", 1)

        cmds.addAttr(dataType="string", hidden=0,
                    longName="hestiaAssetID", shortName="hestiaAsstID")
        cmds.setAttr(currentAsset + ".hestiaAssetID", str(asset.id), type="string")

        cmds.addAttr(dataType="string", hidden=0,
                    longName="hestiaShaderID", shortName="hestiaShdrID")
        cmds.setAttr(currentAsset + ".hestiaShaderID", str(""), type="string")
        
        cmds.addAttr(dataType="string", hidden=0,
                    longName="hestiaVersionID", shortName="hestiaVrsID")
        cmds.setAttr(currentAsset + ".hestiaVersionID", str(version.id), type="string")
        
        # Clear selection.
        cmds.select( clear=True )

        return True
    
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

        if(version.type == ".ma" or version.type == ".mb"):
            # Loading the file.
            cmds.file(new=True, force=True)
            cmds.file(version.outputPath, o=True)

            return True

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
    
    def importAsset(self, version=None):
        """Import the asset inside of Maya.

        Args:
            path (str, optional): Path of the asset. Defaults to "".
        """
        if(self.isInstanceImport(version=version)):
            cmds.file(version.outputPath, reference=True)
        else:
            cmds.file(version.outputPath, i=True)
    
    def isInstanceImport(self, version=None):
        """Return the status for instance import.

        Returns:
            bool: Instance status.
        """
        if(self._instances == True and (version.type == ".ma" or version.type == ".mb")):
            return True
        else:
            return False
    
    def extractAssets(self):
        """Extracts assets for shot building file.
        """
        sceneTransforms = cmds.ls(type="transform")

        for t in sceneTransforms:
            if(cmds.attributeQuery("isHestiaAsset", node=t, exists=True)):
                # Getting data for Hestia assets.
                print("%s : " % t)
                print(cmds.xform(t, query=True, matrix=True, worldSpace=True))

        return False