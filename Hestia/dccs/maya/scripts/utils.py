'''
    :package:   Hestia
    :file:      utils.py
    :author:    ldepoix
    :version:   0.0.3
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
    
    print("Clearing finished")


def upgradeHestiaAttributes():
    """This function clear custom attributes assigned at import.
    """
    print("Start upgrading assets.")
    for currentSelection in cmds.ls(sl=True):
        print("Upgrading %s" % currentSelection)
        if(cmds.attributeQuery("isHestiaAsset", node=currentSelection, exists=True)):
            if(not cmds.attributeQuery("hestiaStaticAsset", node=currentSelection, exists=True)):
                cmds.addAttr(attributeType="bool", hidden=0,
                            longName="hestiaStaticAsset", shortName="hestiaStcAsst")

            if(not cmds.attributeQuery("hestiaAssetID", node=currentSelection, exists=True)):
                cmds.addAttr(dataType="string", hidden=0,
                            longName="hestiaAssetID", shortName="hestiaAsstID")

            if(not cmds.attributeQuery("hestiaShaderID", node=currentSelection, exists=True)):
                cmds.addAttr(dataType="string", hidden=0,
                            longName="hestiaShaderID", shortName="hestiaShdrID")

            if(not cmds.attributeQuery("hestiaVersionID", node=currentSelection, exists=True)):
                cmds.addAttr(dataType="string", hidden=0,
                            longName="hestiaVersionID", shortName="hestiaVrsID")
    print("Upgrading finished")