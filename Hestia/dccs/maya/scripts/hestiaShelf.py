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

   cmds.shelfButton(label='Browser', command='from Hestia.dccs.maya.scripts.launchHestiaBrowser import launchBrowser; launchBrowser()', sourceType='python', annotation='Open Hestia Browser', image='browser.png', style='iconOnly')