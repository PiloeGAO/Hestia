'''
    :package:   Hestia
    :file:      userSetup.py
    :author:    ldepoix
    :version:   0.0.4
    :brief:     Autodesk Maya user setup script.
'''

from maya import utils
from maya import cmds

def initHestiaToolsMenu():
    print("Load Hestia.")

    # Add a menu to the main window.
    cmds.menu("hestiaToolsMenu", label="Hestia", parent="MayaWindow", tearOff=False)

    # Add browser to menu.
    cmds.menuItem("projectBrowser", label="Browser", command="from Hestia.dccs.maya.scripts.launchHestiaBrowser import launchBrowser; launchBrowser()", parent="hestiaToolsMenu")

    cmds.menuItem(divider=True, parent="hestiaToolsMenu")
    cmds.menuItem(subMenu=True, label="UTILS", parent="hestiaToolsMenu")

    # Add clear command to menu.
    cmds.menuItem("clearAttributeTool", label="Clear attributes", command="from Hestia.dccs.maya.scripts.utils import deleteHestiaAttributes; deleteHestiaAttributes()")
    # Add upgrade command to menu.
    cmds.menuItem("upgradeAttributeTool", label="Upgarde attributes", command="from Hestia.dccs.maya.scripts.utils import upgradeHestiaAttributes; upgradeHestiaAttributes()")
    # Adding to submenu.
    cmds.setParent( '..', menu=True )

# Delay execution on UI startup
utils.executeDeferred(initHestiaToolsMenu)