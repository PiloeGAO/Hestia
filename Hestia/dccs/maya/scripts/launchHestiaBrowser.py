'''
    :package:   Hestia
    :file:      launchHestiaBrowser.py
    :author:    ldepoix
    :version:   0.0.5
    :brief:     Class to start UI from Autodesk Maya.
'''
from    maya                            import OpenMayaUI
from    shiboken2                       import wrapInstance
from    PySide2                         import QtWidgets, QtCore

from    Hestia.mainWindow               import MainWindow
from    Hestia.core.manager             import *

def launch_browser():
    """ This function load UI in Maya.
    """
    ptr             = OpenMayaUI.MQtUtil.mainWindow()
    mainWindow      = wrapInstance(int(ptr), QtWidgets.QWidget)

    browser = MainWindow(integration="Maya", parent=mainWindow)
    browser.setWindowFlags(QtCore.Qt.Window)
    browser.show()
    browser = None