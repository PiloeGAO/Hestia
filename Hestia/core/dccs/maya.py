"""
    :package:   Hestia
    :file:      mayaIntegration.py
    :brief:     Maya integration class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import os
import sys

global integrationActive

try:
    from maya import cmds
except:
    integrationActive = False
else:
    integrationActive = True

from ..exceptions import CoreError

from .defaultIntegration import DefaultIntegration

class MayaIntegration(DefaultIntegration):
    """Default integration class.
    """
    def __init__(self, *args, **kwargs):
        super(MayaIntegration, self).__init__(*args, **kwargs)
        self._name = "Maya"

        if(not integrationActive):
            self._manager.logging.error("Maya Libraries not found!")

        self._active = integrationActive

        # Initialize file formats.
        self._manager.logging.info("Initialize File Formats.")
        self._default_format = "ma"
        self._available_formats = ["ma", "mb"]

        # Load necessary plugins for Hestia (including mayausd).
        plugins = {
            "tools" : [
                "timeSliderBookmark",
            ],
            "extensions" : [
                {
                    "mayaUsdPlugin,mtoh": ["usda", "usdc", "usd"],
                }
            ]
        }
        self.initialize_plugins(plugins=plugins)

        # Get the current render engine (WARNING: Multiple render engine not supported).
        self._current_render_engine = "legacy"
        self.check_render_engine()

        self._support_screenshots   = True
    
    def initialize_plugins(self, plugins={}):
        """Initialize the file formats list.

        Returns:
            list: str: File formats enables.
        """
        if(sys.platform.startswith('win32')):
            plugin_extension = "mll"
        elif(sys.platform.startswith('darwin')):
            plugin_extension = "bundle"
        else:
            raise CoreError("Linux not supported.")

        # Enabling plugins for additional formats
        for tool in plugins["tools"]:
            self.load_maya_plugin("{}.{}".format(tool, plugin_extension))

        for extensions in plugins["extensions"]:
            for plugins in extensions:
                for plugin in plugins.split(","):
                    status = self.load_maya_plugin("{}.{}".format(plugin, plugin_extension))

                self._available_formats.extend(extensions[plugins])
    
    def load_maya_plugin(self, plugin_name):
        """Load external plugins needed by the implementation (exemple: for special formats...)
        
        Args:
            plugin_name (str): Name of the plugin.

        Returns:
            bool: Status of the loading.
        """
        try:
            cmds.loadPlugin(plugin_name)
            return True
        except RuntimeError:
            raise CoreError("Failed to load {}.{}".format(plugin, plugin_extension))
    
    def check_render_engine(self):
        """Check plugin list to get renderer's names.
        """
        plugin_list = cmds.pluginInfo(query=True, listPlugins=True)

        if("mtoa" in plugin_list):
            self._current_render_engine = "arnold"
        else:
            self._current_render_engine = "legacy"

    
    def load_asset(self, asset=None, version=None, staticAsset=None):
        """Load the selected asset inside of the scene.

        Args:
            asset (class:"Entity"): Asset datas. Defaults to None.
            version (class:"Version"): Version datas. Defaults to None.

        Returns:
            bool: load status.
        """
        if(not os.path.exists(version.output_path)):
            self._manager.logging.error("File not found.")
            return False

        return True
    
    def load_shot(self, asset=None, version=None):
        """Load the selected shot inside of the scene.

        Args:
            asset (class:"Entity"): Asset datas. Defaults to None.
            version (class:"Version"): Version datas. Defaults to None.

        Returns:
            bool: load status.
        """
        if(not os.path.exists(version.output_path)):
            self._manager.logging.error("File not found.")
            return False

        if(version.type == ".ma" or version.type == ".mb"):
            # Loading the file.
            cmds.file(new=True, force=True)
            cmds.file(version.output_path, o=True)

            return True
        else:
            return False
    
    def setup_shot(self, category=None, shot=None):
        """Setup shot values (eg: Framerate, duration, camera...) inside of the scene.

        Args:
            category (class: "Category"): Categrory datas. Defaults to None.
            shot (class: "Entity"): Shot datas. Defaults to None.

        Returns:
            bool: Setup status.
        """
        try:
            from maya.plugin.timeSliderBookmark.timeSliderBookmark import createBookmark
        except Exception as e:
            raise CoreError("timeSliderBookmark not loaded in Maya.")
        project = get_current_project()

        # Checking if the file current file is part of a maya projet foldertree.
        filepath = cmds.file(q=True, sn=True)

        if(filepath != ""):
            if(os.path.basename(os.path.dirname(filepath)) == "scenes" and
                os.path.isfile(os.path.dirname(filepath) + os.sep + ".." + os.sep + "workspace.mel")):
                self._manager.logging.debug("The scene is part of a Maya Project, Hestia will setup the project correctly! ")
                cmds.workspace(os.path.abspath(os.path.dirname(filepath) + os.sep + ".."), openWorkspace=True)
            else:
                self._manager.logging.warning("The scene isn't part of a Maya Project, please build a Maya project and save your scene in the \"scenes\" subdirectory (all features couldn't work as expected).")
        else:
            self._manager.logging.warning("Please save your scene (all features couldn't work as expected).")

        # Set main values for timeline setup.
        # Correct order is:
        # |-----------------------------------------------------------------------------|
        # | start_frame | start_animation_frame ======> end_animation_frame | end_frame |
        # |-----------------------------------------------------------------------------|
        start_frame           = project.start_frame
        start_animation_frame = start_frame + project.pre_roll
        end_animation_frame   = start_animation_frame + shot.frame_number
        end_frame             = end_animation_frame + project.post_roll

        # Set timeline datas.
        cmds.currentUnit( time='%sfps' % int(project.framerate)) # WARNING: Framerate must be setup before timeline !

        cmds.playbackOptions(animationStartTime=start_frame, minTime=start_animation_frame,
                            animationEndTime=end_frame,      maxTime=end_animation_frame,
                            playbackSpeed=1.0)

        # Create timeline bookmarks (for visual feedback).
        # "timeSliderBookmark.mll" need to be loaded first.
        createBookmark(name="PREROLL",  start=start_frame,            stop=(start_animation_frame-1), color=(0.67, 0.23, 0.23))
        createBookmark(name="ANIM",     start=start_animation_frame,   stop=end_animation_frame,       color=(0.28, 0.69, 0.48))
        createBookmark(name="POSTROLL", start=(end_animation_frame+1), stop=end_frame,                color=(0.67, 0.23, 0.23))

        # Setting up render settings in the scene.
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix", "%s_%s_<Scene>_<RenderLayer>_<Camera>" % (category.name, shot.name), type="string")

        width, height = project.resolution
        cmds.setAttr("defaultResolution.width", width)
        cmds.setAttr("defaultResolution.height", height)

        cmds.setAttr("defaultRenderGlobals.start_frame", start_animation_frame)
        cmds.setAttr("defaultRenderGlobals.end_frame", end_animation_frame)
        cmds.setAttr("defaultRenderGlobals.byFrameStep", 1.0)

        cmds.setAttr("defaultRenderGlobals.animation", True)
        cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt", True)

        # Getting the number of digits from last frame to set padding.
        padding_count = 0
        counter = end_frame
        while(counter>0):
            padding_count=padding_count+1
            counter=counter//10

        cmds.setAttr("defaultRenderGlobals.extensionPadding", padding_count)

        return True
    
    def take_playblast(self, start_frame, end_frame, path):
        """Take a playblast of the scene.

        Args:
            start_frame (int): Start frame.
            end_frame (int): End frame.
            path (sty): Ouput path.

        Returns:
            bool: Function status.
        """
        # set screenshot dimensions
        width = 1920
        height = 1080

        if(start_frame == end_frame):
            # From: https://gist.github.com/gfxhacks/f3e750f416f94952d7c9894ed8f78a71
            # Take a single image.
            currentFrame = start_frame
            if(start_frame == -1):
                currentFrame = int(cmds.currentTime(query=True))

            cmds.playblast(fr=currentFrame, v=False, fmt="image", c="png", orn=False, cf=path, wh=[width,height], p=100, forceOverwrite=True)
        else:
            # TODO: Use framerange from inputs.
            # Take a video.
            cmds.playblast(v=False, orn=False, f=path, wh=[width,height], p=100, forceOverwrite=True)

        return True

    def open_file(self, version):
        """Open the file in the DCC.

        Args:
            version (class:`Version`): Version of the asset.

        Returns:
            bool: Function status.
        """
        filePath = str(version.working_path)
        if(os.path.isfile(filePath) and
            (os.path.splitext(filePath)[1] == ".ma" or os.path.splitext(filePath)[1] == ".mb")):
            cmds.file(new=True, force=True)
            cmds.file(version.working_path, o=True)
            return True
        else:
            return False
    
    def save_file(self, path):
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
        
        self._manager.logging.error("Failed to save the file : %s" % path)
        return False

    def export_selection(self, path, extension):
        """Export selection to the path with the correct format.

        Args:
            path (str): Output path.
            extension (str): Extensionof the file.

        Returns:
            bool: Function status.
        """
        if(os.path.isfile(path)):
            self._manager.logging.error("File \"%s\" already exist, skipping export." % path)
            return False
        
        if(len(cmds.ls(sl=True)) == 0):
            self._manager.logging.error("Nothing selected, skipping export.")
            return False
        
        extension = extension.lower()

        if(extension == ".ma"):
            cmds.file(path, type='mayaAscii', exportSelected=True)
        elif(extension == ".mb"):
            cmds.file(path, type='mayaBinary', exportSelected=True)
        else:
            return False
        
        return True