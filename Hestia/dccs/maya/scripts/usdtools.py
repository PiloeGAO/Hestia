'''
    :package:   Hestia
    :file:      usdtools.py
    :author:    ldepoix
    :version:   0.0.5
    :brief:     Functions to manage USD inside of Autodesk Maya.
'''
import os

from maya import cmds

from Hestia.core.dccs.maya import MayaIntegration
from Hestia.core.USD.tools import USDTools

MAYA_PYTHON_INTERPRETER = MayaIntegration.get_interpreter()

def open_usdview():
    """ This function open USD View in Maya.
    """
    filters = "USD Files (*.usd *.usdc *.usda *.usdz);;All Files (*.*)"

    filepaths = cmds.fileDialog2(fileFilter=filters,
        fileMode=1,
        okCaption="Open")

    if(filepaths == None):
        return

    USDTools.open_usdview(filepaths[0], interpreter=MAYA_PYTHON_INTERPRETER)

def open_usdcat():
    """ This function open USD Cat in Maya.
    """
    filters = "USD Files (*.usd *.usdc *.usda *.usdz);;All Files (*.*)"

    filepaths = cmds.fileDialog2(fileFilter=filters,
        fileMode=1,
        okCaption="Open")

    if(filepaths == None):
        return

    output = "{}.usda".format(os.path.splitext(filepaths[0])[0])

    USDTools.open_usdcat(filepaths[0], interpreter=MAYA_PYTHON_INTERPRETER, output=output)