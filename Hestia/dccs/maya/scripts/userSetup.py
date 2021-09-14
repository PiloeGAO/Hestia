'''
    :package:   Hestia
    :file:      userSetup.py
    :author:    ldepoix
    :version:   0.0.5
    :brief:     Autodesk Maya user setup script.
'''

from maya import utils
from maya import cmds

from Hestia.dccs.maya.scripts.hestia_shelf import create_hestia_shelf

def init_hestia_menu():
    print("Load Hestia.")

    # Add a menu to the main window.
    cmds.menu("hestiaToolsMenu", label="Hestia", parent="MayaWindow", tearOff=False)

    # Add browser to menu.
    cmds.menuItem("projectBrowser", label="Browser", command="from Hestia.dccs.maya.scripts.launch_hestia_browser import launch_browser; launch_browser()", parent="hestiaToolsMenu")
    
    cmds.menuItem( divider=True )

    # Add USD Tools.
    cmds.menuItem("USDView_open", label="USD View", command="from Hestia.dccs.maya.scripts.usdtools import open_usdview; open_usdview()", parent="hestiaToolsMenu")
    cmds.menuItem("USDCat_open", label="USD Cat", command="from Hestia.dccs.maya.scripts.usdtools import open_usdcat; open_usdcat()", parent="hestiaToolsMenu")

# Delay execution on UI startup
utils.executeDeferred(init_hestia_menu)
utils.executeDeferred(create_hestia_shelf)