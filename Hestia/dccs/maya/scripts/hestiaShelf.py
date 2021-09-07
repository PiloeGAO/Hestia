'''
    :package:   Hestia
    :file:      shelf.py
    :author:    ldepoix
    :version:   0.0.5
    :brief:     Maya shelf (source: arnoldShelf.py [mtoa plugin]).
'''
import maya.cmds as cmds
import maya

def removeHestiaShelf():
   if cmds.shelfLayout('Hestia', exists=True):
      cmds.deleteUI('Hestia')

def createHestiaShelf():
   removeHestiaShelf()
   shelfTab = maya.mel.eval('global string $gShelfTopLevel;')
   maya.mel.eval('global string $hestiaShelf;')
   maya_version = int(cmds.about(version=True))
   if maya_version < 2017:
      maya.mel.eval('$hestiaShelf = `shelfLayout -cellWidth 32 -cellHeight 32 -p $gShelfTopLevel Hestia`;')   
   else:
      maya.mel.eval('$hestiaShelf = `shelfLayout -cellWidth 32 -cellHeight 32 -p $gShelfTopLevel -version \"2017\" Hestia`;')

   shelfStyle = ('shelf' if maya_version >= 2016 else 'simple')

   # Please add the icons folder to environment variable: XBMLANGPATH
   cmds.shelfButton(label='Browser', command='from Hestia.dccs.maya.scripts.launchHestiaBrowser import launch_browser; launch_browser()', sourceType='python', annotation='Open Hestia Browser', image='cloud.png', style='iconOnly')
   cmds.shelfButton(label='SEPARATOR', command='', sourceType='python', annotation='', image='safety_divider_custom.png', style='iconOnly')
   cmds.shelfButton(label='USD View', command='from Hestia.dccs.maya.scripts.usdtools import open_usdview; open_usdview()', sourceType='python', annotation='Open USD View', image='launch.png', style='iconOnly')
   cmds.shelfButton(label='USD Cat', command='from Hestia.dccs.maya.scripts.usdtools import open_usdcat; open_usdcat()', sourceType='python', annotation='Open USD Cat', image='transform.png', style='iconOnly')