"""
    :package:   Hestia
    :file:      encoding.py
    :brief:     encoding utility functions.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import sys
import os
import subprocess

def video_converter(filePath, targetPath):
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