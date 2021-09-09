"""
    :package:   Hestia
    :file:      encoding.py
    :brief:     encoding utility functions.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import sys
import os
import shutil
from .command import run_shell_command

from ..logger import get_logging
logging = get_logging(__name__)

def video_converter(file_path, target_path, codec="h264"):
    """Convert video to MP4.

    Args:
        file_path (str): Input path.
        target_path (str): Ouput path.

    Returns:
        bool: Convert status.
    """
    file_path = file_path.replace("\\", "/")
    target_path = target_path.replace("\\", "/")

    if(codec == "h264"):
        args = "-vcodec libx264 -acodec aac"
    else:
        logging.error("Converter only support h264.")
        return False

    ffmpeg_exe = "ffmpeg"
    if(sys.platform.startswith("win32")):
        ffmpeg_exe = "ffmpeg.exe"

    if(not shutil.which(ffmpeg_exe)):
        logging.error("FFMPEG not in path, conversion can't be done.")
        return False
    
    run_shell_command(f"{ffmpeg_exe} -i {file_path} {args} {target_path}", shell=True, get_log=True)

    if(not os.path.isfile(target_path)):
        logging.error("Conversion failed, please contact your TD.")
        return False

    return True