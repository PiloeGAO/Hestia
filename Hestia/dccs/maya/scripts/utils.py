'''
    :package:   Hestia
    :file:      utils.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     Utils functions for Hestia.
'''

from    maya                            import cmds

def deleteHestiaAttributes():
    """This function clear custom attributes assigned at import.
    """
    for currentSelection in cmds.ls(sl=True):
        if(cmds.attributeQuery("isHestiaAsset", node=currentSelection, exists=True)):
            cmds.deleteAttr(currentSelection, at="isHestiaAsset")
            cmds.deleteAttr(currentSelection, at="hestiaAssetID")
            cmds.deleteAttr(currentSelection, at="hestiaShaderID")
            cmds.deleteAttr(currentSelection, at="hestiaVersionID")