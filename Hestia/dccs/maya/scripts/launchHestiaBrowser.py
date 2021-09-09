'''
    :package:   Hestia
    :file:      launchHestiaBrowser.py
    :author:    ldepoix
    :version:   0.0.5
    :brief:     Class to start UI from Autodesk Maya.
'''
from .dockable_widget import DockableWidgetUIScript

from    Hestia.mainWindow               import MainWindow
from    Hestia.core.manager             import *

def launch_browser():
    """ This function load UI in Maya.
    """
    browser_widget = MainWindow(integration="Maya")
    DockableWidgetUIScript("Hestia Browser", browser_widget)