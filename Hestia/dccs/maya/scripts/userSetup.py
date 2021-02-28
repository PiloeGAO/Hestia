'''
    :package:   Hestia
    :file:      userSetup.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     Autodesk Maya user setup script.
'''

from maya import utils
from maya import cmds

def initHestiaToolsMenu():
    print("Loading Hestia Menu.")

    # Add a menu to the main window.
    cmds.menu("hestiaToolsMenu", label="Hestia", parent="MayaWindow", tearOff=False)

    # Add new menu item.
    cmds.menuItem("projectBrowser", label="Browser", command="from Hestia.dccs.maya.scripts.launchHestiaBrowser import launchBrowser; launchBrowser()", parent="hestiaToolsMenu")

# Delay execution on UI startup
utils.executeDeferred(initHestiaToolsMenu)