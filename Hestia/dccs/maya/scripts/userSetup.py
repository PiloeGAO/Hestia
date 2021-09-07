'''
    :package:   Hestia
    :file:      userSetup.py
    :author:    ldepoix
    :version:   0.0.5
    :brief:     Autodesk Maya user setup script.
'''

from maya import utils
from maya import cmds

from Hestia.dccs.maya.scripts.hestiaShelf import createHestiaShelf

def initHestiaToolsMenu():
    print("Load Hestia.")

    # Add a menu to the main window.
    cmds.menu("hestiaToolsMenu", label="Hestia", parent="MayaWindow", tearOff=False)

    # Add browser to menu.
    cmds.menuItem("projectBrowser", label="Browser", command="from Hestia.dccs.maya.scripts.launchHestiaBrowser import launch_browser; launch_browser()", parent="hestiaToolsMenu")

# Delay execution on UI startup
utils.executeDeferred(initHestiaToolsMenu)
utils.executeDeferred(createHestiaShelf)