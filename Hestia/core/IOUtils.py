"""
    :package:   Hestia
    :file:      IOUtils.py
    :brief:     IO functions.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
"""
import sys, os, shutil, subprocess

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
            dst = targetPath + os.sep + kwargs["newName"] + os.path.splitext(oldFilename)[1]
            if(os.path.isfile(dst) != True):
                src = targetPath + os.sep + oldFilename
                os.rename(src, dst)

        return True
    return False

def videoConverter(filePath, targetPath):
    """Convert video to MP4.

    Args:
        filePath (str): Input path.
        targetPath (str): Ouput path.

    Returns:
        bool: Convert status.
    """
    ffmpeg_installDir = os.path.dirname(os.path.abspath(__file__)) + os.sep + "ffmpeg" + os.sep + "bin"

    # TODO: Support MacOS and Linux.
    if(os.path.isdir(ffmpeg_installDir) and sys.platform.startswith("win32")):
        ffmepg_exe = ffmpeg_installDir + os.sep + "ffmpeg.exe"
        subprocess.call("%s -i %s -vcodec libx264 -acodec aac %s" % (ffmepg_exe, filePath, targetPath))
        return True

    return False