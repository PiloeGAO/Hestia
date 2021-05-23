"""
    :package:   Hestia
    :file:      mayaIntegration.py
    :brief:     Maya integration class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.3
"""
import os

global integrationActive

try:
    from maya import cmds
    from maya.plugin.timeSliderBookmark.timeSliderBookmark import createBookmark
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

        self._name = "Maya"

        if(not integrationActive):
            self.__manager.logging.error("Maya Libraries not found!")

        self._active = integrationActive

        self._defaultFormat = ".ma"
        self.initializeFileFormats()

        # Autodesk Maya support instance by using "References". 
        self._supportInstances      = True
        self._instances             = True
        self._supportScreenshots    = True
    
    def initializeFileFormats(self):
        """Initialize the file formats list.

        Returns:
            list: str: File formats enables.
        """
        self.__manager.logging.info("Initialize File Formats.")
        self._availableFormats = [".ma", ".mb"]

        # Enabling plugins for additional formats
        pluginFormats = {".obj": ["objExport.mll"], ".abc": ["AbcExport.mll", "AbcImport.mll"]}
        for plugin in pluginFormats:
            for subPlugin in pluginFormats[plugin]:
                loadPluginStatus = self.loadExternalPlugin(pluginName=subPlugin)
                if(loadPluginStatus is not True):
                    break

            if(loadPluginStatus):
                self._availableFormats.append(plugin)
        
        # Enabling plugins for additional features.
        plugins = ["timeSliderBookmark.mll"]
        for plugin in plugins:
            loadPluginStatus = self.loadExternalPlugin(pluginName=plugin)
    
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

        # Looking for asset replacement.
        currentSelection = cmds.ls(sl=True)
        if(len(currentSelection) > 0):
            currentSelection = currentSelection[0]
            if(cmds.attributeQuery("isHestiaAsset", node=currentSelection, exists=True)):
                if(cmds.getAttr(currentSelection+".hestiaAssetID") == str(asset.id)):
                    if(cmds.objectType(currentSelection) == "reference" and self.isInstanceImport(version=version)):
                        # Updating reference is done with the file function. From: https://stackoverflow.com/a/44718215
                        referenceToUpdate = cmds.referenceQuery(currentSelection, referenceNode=True)
                        cmds.file(version.outputPath, loadReference=referenceToUpdate)
                    elif(cmds.objectType(currentSelection) == "transform" and not self.isInstanceImport(version=version)):
                        # Delete objects inside of the selected group.
                        oldObjects = cmds.listRelatives(currentSelection, children=True)
                        cmds.delete(oldObjects)

                        # Importing the asset and getting the transform node.
                        before = set(cmds.ls(type="transform"))

                        self.importAsset(asset=asset, version=version)

                        after = set(cmds.ls(type="transform"))
                        imported = after - before

                        # Reparent new objects.
                        cmds.parent(imported, currentSelection, relative=True)
                        
                        #Rename each object to avoid duplication on second import.
                        for object in imported:
                            cmds.rename(object, "%s_%s" % (currentSelection, object))
                    else:
                        self.__manager.logging.warning("Reference and traditional import can't be mixed together.")
                        return False
                    
                    return True

        # If nothing is selected or asset isn't the same, start import procedure.
        currentAsset = None    
        # Create a group that will contain asset except for instances.
        if(not self.isInstanceImport(version=version)):
            # Importing the asset and getting the transform node.
            before = set(cmds.ls(type="transform"))

            self.importAsset(asset=asset, version=version)

            after = set(cmds.ls(type="transform"))
            imported = after - before

            staticAsset = 1
            groupName = asset.name.replace(" ", "_").replace("-", "_")

            while(cmds.objExists(groupName) or groupName in cmds.namespaceInfo(listNamespace=True)):
                groupName = groupName + "_bis"

            # Group need to be created as empty to make sure pivot is in the center of the scene.
            cmds.group(empty=True, name=groupName, absolute=True)
            cmds.parent(imported, groupName, relative=True)

            #Rename each object to avoid duplication on second import.
            for object in imported:
                cmds.rename(object, "%s_%s" % (groupName, object))

            cmds.select(groupName, r=True)
            currentAsset = cmds.ls(sl=True)[0]
        else:
            # Importing the asset and getting the reference node.
            before = set(cmds.ls(type="reference"))

            self.importAsset(asset=asset, version=version)

            after = set(cmds.ls(type="reference"))
            imported = after - before

            staticAsset = 0

            cmds.select(imported, r=True)
            currentAsset = cmds.ls(sl=True)[0]

            # I need to unlock the reference to add custom attributes
            # Source: https://discourse.techart.online/t/adding-attributes-to-a-reference-node-in-maya/9274
            cmds.getAttr(currentAsset + ".locked")
            cmds.lockNode(currentAsset,q=1,lock=1)
            cmds.lockNode(currentAsset,lock=0)

        # Setting needed attributes for shot assembly.
        cmds.addAttr(attributeType="bool", hidden=0,
                    longName="isHestiaAsset", shortName="isHstAsst")
        cmds.setAttr(currentAsset + ".isHestiaAsset", 1)
        
        cmds.addAttr(attributeType="bool", hidden=0,
                    longName="hestiaStaticAsset", shortName="hestiaStcAsst")
        cmds.setAttr(currentAsset + ".hestiaStaticAsset", staticAsset)

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
    
    def setupShot(self, category=None, shot=None):
        """Setup shot values (eg: Framerate, duration, camera...) inside of the scene.

        Args:
            category (class: "Category"): Categrory datas. Defaults to None.
            shot (class: "Entity"): Shot datas. Defaults to None.

        Returns:
            bool: Setup status.
        """
        project = self.__manager.projects[self.__manager.currentProject]

        # Checking if the file current file is part of a maya projet foldertree.
        filepath = cmds.file(q=True, sn=True)

        if(filepath != ""):
            if(os.path.basename(os.path.dirname(filepath)) == "scenes" and
                os.path.isfile(os.path.dirname(filepath) + os.sep + ".." + os.sep + "workspace.mel")):
                self.__manager.logging.debug("The scene is part of a Maya Project, Hestia will setup the project correctly! ")
                cmds.workspace(os.path.abspath(os.path.dirname(filepath) + os.sep + ".."), openWorkspace=True)
            else:
                self.__manager.logging.warning("The scene isn't part of a Maya Project, please build a Maya project and save your scene in the \"scenes\" subdirectory (all features couldn't work as expected).")
        else:
            self.__manager.logging.warning("Please save your scene (all features couldn't work as expected).")

        # Set main values for timeline setup.
        # Correct order is:
        # |-----------------------------------------------------------------------|
        # | startFrame | startAnimationFrame ======> endAnimationFrame | endFrame |
        # |-----------------------------------------------------------------------|
        startFrame          = project.startFrame
        startAnimationFrame = startFrame + project.preRoll
        endAnimationFrame   = startAnimationFrame + shot.frameNumber
        endFrame            = endAnimationFrame + project.postRoll

        # Set timeline datas.
        cmds.currentUnit( time='%sfps' % int(project.framerate)) # WARNING: Framerate must be setup before timeline !

        cmds.playbackOptions(animationStartTime=startFrame, minTime=startAnimationFrame,
                            animationEndTime=endFrame,      maxTime=endAnimationFrame,
                            playbackSpeed=1.0)

        # Create timeline bookmarks (for visual feedback).
        # "timeSliderBookmark.mll" need to be loaded first.
        createBookmark(name="PREROLL",  start=startFrame,            stop=(startAnimationFrame-1), color=(0.67, 0.23, 0.23))
        createBookmark(name="ANIM",     start=startAnimationFrame,   stop=endAnimationFrame,       color=(0.28, 0.69, 0.48))
        createBookmark(name="POSTROLL", start=(endAnimationFrame+1), stop=endFrame,                color=(0.67, 0.23, 0.23))

        # Setting up render settings in the scene.
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix", "%s_%s_<Scene>_<RenderLayer>_<Camera>" % (category.name, shot.name), type="string")

        width, height = project.resolution
        cmds.setAttr("defaultResolution.width", width)
        cmds.setAttr("defaultResolution.height", height)

        cmds.setAttr("defaultRenderGlobals.startFrame", startAnimationFrame)
        cmds.setAttr("defaultRenderGlobals.endFrame", endAnimationFrame)
        cmds.setAttr("defaultRenderGlobals.byFrameStep", 1.0)

        cmds.setAttr("defaultRenderGlobals.animation", True)
        cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt", True)

        # Getting the number of digits from last frame to set padding.
        paddingCount = 0
        counter = endFrame
        while(counter>0):
            paddingCount=paddingCount+1
            counter=counter//10

        cmds.setAttr("defaultRenderGlobals.extensionPadding", paddingCount)

        return True
    
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
        """Import the asset inside of Maya.

        Args:
            path (str, optional): Path of the asset. Defaults to "".
        """
        if(self.isInstanceImport(version=version)):
            cmds.file(version.outputPath, reference=True, usingNamespaces=True, namespace=asset.name)
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
    
    def assignShaderToSelectedAsset(self, version):
        """Assign a shader ID to an Hestia asset.

        Args:
            version (class:"Version"): Version datas. Defaults to None.

        Returns:
            bool: Function status.
        """
        if(len(cmds.ls(sl=True)) == 0):
            return False
        
        currentAsset = cmds.ls(sl=True)[0]

        if(cmds.attributeQuery("isHestiaAsset", node=currentAsset, exists=True)
                and cmds.attributeQuery("hestiaShaderID", node=currentAsset, exists=True)):
            cmds.setAttr(currentAsset + ".hestiaShaderID", str(version.id), type="string")
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
    
    def openFile(self, version):
        """Open the file in the DCC.

        Args:
            version (class:`Version`): Version of the asset.

        Returns:
            bool: Function status.
        """
        filePath = str(version.workingPath)
        if(os.path.isfile(filePath) and
            (os.path.splitext(filePath)[1] == ".ma" or os.path.splitext(filePath)[1] == ".mb")):
            cmds.file(new=True, force=True)
            cmds.file(version.workingPath, o=True)
            return True
        else:
            return False
    
    def saveFile(self, path):
        """Save current file to the given path.

        Args:
            path (str): File path.

        Returns:
            bool: Functions status.
        """
        if(not os.path.isfile(path)):
            cmds.file(rename=path)
            cmds.file(force=True, save=True, type="mayaAscii")
            return True
        
        return False

    def exportSelection(self, path, extension):
        """Export selection to the path with the correct format.

        Args:
            path (str): Output path.
            extension (str): Extensionof the file.

        Returns:
            bool: Function status.
        """
        if(os.path.isfile(path)):
            self.__manager.logging.error("File \"%s\" already exist, skipping export." % path)
            return False
        
        if(len(cmds.ls(sl=True)) == 0):
            self.__manager.logging.error("Nothing selected, skipping export.")
            return False
        
        extension = extension.lower()

        if(extension == ".ma"):
            cmds.file(path, type='mayaAscii', exportSelected=True)
        elif(extension == ".mb"):
            cmds.file(path, type='mayaBinary', exportSelected=True)
        elif(extension == ".abc"):
            oldSelection = cmds.ls(sl=True)

            # Select hierarchy.
            cmds.select(hierarchy=True)
            command = "-uvWrite -worldSpace " + "-selection -file " + path
            cmds.AbcExport ( j = command )

            # Reset selection
            cmds.select(oldSelection)
        elif(extension == ".obj"):
            cmds.file(path, type='OBJexport', exportSelected=True)
        else:
            return False
        
        return True