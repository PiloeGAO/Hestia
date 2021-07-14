'''
    :package:   Hestia
    :file:      launchHestiaBrowser.py
    :author:    ldepoix
    :version:   0.0.4
    :brief:     Class to start UI from Autodesk Maya.
'''
from    maya                            import OpenMayaUI
from    shiboken2                       import wrapInstance
from    PySide2                         import QtWidgets, QtCore

from    Hestia.mainWindow               import MainWindow
from    Hestia.core.manager             import *

def launchBrowser():
    """ This function load UI in Maya.
    """
    ptr             = OpenMayaUI.MQtUtil.mainWindow()
    mainWindow      = wrapInstance(ptr, QtWidgets.QWidget)

    browser = MainWindow(integration="Maya", parent=mainWindow)
    browser.setWindowFlags(QtCore.Qt.Window)
    browser.show()
    browser = None