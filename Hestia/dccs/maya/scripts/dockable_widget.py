'''
    :package:   Hestia
    :file:      dockable_widget.py
    :author:    ldepoix
    :version:   0.0.5
    :brief:     Maya dockable widget (source: devkit/pythonScripts/dockableWorkspaceWidget.py).
'''
from builtins import int
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
from maya import OpenMayaUI

from shiboken2 import wrapInstance
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout

customMixinWindow = None

class DockableWidget(MayaQWidgetDockableMixin, QWidget):
    """Custom Maya dockable widget.

    Args:
        window_title (str): Window Title
        widget (class: `QWidget`): Widget to use in the window.
        parent (None, optional): - . Defaults to None.
    """
    toolName = 'customDockableWidget'

    def __init__(self, window_title, widget, parent=None):
        # Delete any previous instances that is detected. Do this before parenting self to main window!
        self.deleteInstances()

        super(DockableWidget, self).__init__(parent=parent)

        layout = QVBoxLayout()
        layout.addWidget(widget)
        self.setLayout(layout)
        self.setWindowTitle(window_title)

    def dockCloseEventTriggered(self):
        self.deleteInstances()

    def closeEvent(self, event):
        """Get the close event on window close.

        Args:
            event (class: 'QtEvent'): Event.
        """
        self.deleteInstances()
        event.accept()

    # Delete any instances of this class
    def deleteInstances(self):
        """Source: https://stackoverflow.com/a/58399801
        """
        mayaMainWindowPtr = OpenMayaUI.MQtUtil.mainWindow() 
        mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QMainWindow) # Important that it's QMainWindow, and not QWidget/QDialog

        # Go through main window's children to find any previous instances
        for obj in mayaMainWindow.children():
            if type( obj ) == MayaQDockWidget:
                if obj.widget().objectName() == self.__class__.toolName: # Compare object names
                    # If they share the same name then remove it
                    print("Deleting instance {0}".format(obj))
                    mayaMainWindow.removeDockWidget(obj) # This will remove from right-click menu, but won't actually delete it! ( still under mainWindow.children() )
                    # Delete it for good
                    obj.setParent(None)
                    obj.deleteLater()
   
def DockableWidgetUIScript(window_name="Dockable Widget", widget=None, restore=False):
    """Util function to initialize the Custom Dockable widget.

    Args:
        window_name (str, optional): Window name. Defaults to "Dockable Widget".
        widget (class: `QWidget`, optional): Widget to assign. Defaults to None.
        restore (bool, optional): Use the restore functionality. Defaults to False.

    Returns:
        class: `DockableWidget`: Class initialized.
    """
    global customMixinWindow
  
    if restore == True:
        # Grab the created workspace control with the following.
        restoredControl = OpenMayaUI.MQtUtil.getCurrentParent()
  
    if customMixinWindow is None:
        # Create a custom mixin widget for the first time
        customMixinWindow = DockableWidget(window_name, widget)
        customMixinWindow.setObjectName(f"{window_name}Window".replace(" ", "_"))
      
    if restore == True:
        # Add custom mixin widget to the workspace control
        mixinPtr = OpenMayaUI.MQtUtil.findControl(customMixinWindow.objectName())
        OpenMayaUI.MQtUtil.addWidgetToMayaLayout(int(mixinPtr), int(restoredControl))
    else:
        # Create a workspace control for the mixin widget by passing all the needed parameters. See workspaceControl command documentation for all available flags.
        customMixinWindow.show(dockable=True, width=1280, height=720)
      
    return customMixinWindow