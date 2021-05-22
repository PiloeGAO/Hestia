"""
    :package:   Hestia
    :file:      IOUtils.py
    :brief:     IO functions.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.3
"""
import os, shutil

def makeFolder(path):
    """Build a folder.

    Args:
        path (str): Folder path.

    Returns:
        bool: Creation status.
    """
    if(not os.path.isdir(path)):
        try:
            os.makedirs(path)
        except OSError as error:
            print("Directory %s can't be created (%s)" % (path, error))
            return False
        else:
            return True
    else:
        return False

def copyFile(filePath, targetPath, **kwargs):
    """Copy a file from a directory to another.

    Args:
        filePath (str): Input path.
        targetPath (str): Ouput path.

    Returns:
        bool: Copy status.
    """
    oldFilename = os.path.split(filePath)[1]
    if( not os.path.isfile(targetPath + os.sep + oldFilename)):
        shutil.copy(filePath, targetPath)

        if(kwargs["newName"] != None):
            src = targetPath + os.sep + oldFilename
            dst = targetPath + os.sep + kwargs["newName"] + os.path.splitext(oldFilename)[1]
            os.rename(src, dst)

        return True
    return False