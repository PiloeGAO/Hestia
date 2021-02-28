'''
    :package:   Hestia
    :file:      launchHestiaBrowser.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     Class to start UI from Autodesk Maya.
'''

from    maya                            import OpenMayaUI
from    shiboken2                       import wrapInstance
from    PySide2                         import QtWidgets

from    Hestia.mainWindow                import MainWindow

def launchBrowser():
    """ This function load UI in Maya.
    """
    ptr             = OpenMayaUI.MQtUtil.mainWindow()
    mainWindow      = wrapInstance(long(ptr), QtWidgets.QWidget)

    browser = MainWindow(mode="kitsu")
    browser.show()