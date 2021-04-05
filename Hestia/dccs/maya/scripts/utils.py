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
    print("Start Clearing.")
    for currentSelection in cmds.ls(sl=True):
        print("Clearing %s" % currentSelection)
        if(cmds.attributeQuery("isHestiaAsset", node=currentSelection, exists=True)):
            cmds.deleteAttr(currentSelection, at="isHestiaAsset")
        if(cmds.attributeQuery("hestiaStaticAsset", node=currentSelection, exists=True)):
            cmds.deleteAttr(currentSelection, at="hestiaStaticAsset")
        if(cmds.attributeQuery("hestiaAssetID", node=currentSelection, exists=True)):
            cmds.deleteAttr(currentSelection, at="hestiaAssetID")
        if(cmds.attributeQuery("hestiaShaderID", node=currentSelection, exists=True)):
            cmds.deleteAttr(currentSelection, at="hestiaShaderID")
        if(cmds.attributeQuery("hestiaVersionID", node=currentSelection, exists=True)):
            cmds.deleteAttr(currentSelection, at="hestiaVersionID")
    
    print("Clearing finished for selection")