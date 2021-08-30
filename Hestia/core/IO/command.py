"""
    :package:   Hestia
    :file:      command.py
    :brief:     Command util to start subprocesses.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import shlex
import subprocess

from ..exceptions import CoreError

from ..logger import get_logging
logging = get_logging(__name__)

def run_shell_command(command_line):
    """Start a command with subprocess and log outputs.

    FOR MAYA: https://discourse.techart.online/t/run-maya-and-execute-a-script/11999/7
    Add python case in each dccs, with argument in this command in case of python command.
    
    Args:
        command_line (str): Command.
    """
    if(type(command_line) != list):
        command_line_args = shlex.split(command_line)
    else:
        command_line_args = command_line

    logging.info("Starting following command: {}".format(" ".join(command_line_args)))

    try:
        command_line_process = subprocess.Popen(
            command_line_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            shell=False
        )

        # FOR DEBUG ONLY (freeze the main thread, threading management should be added later):
        # logging.debug(command_line_process.communicate()[1].decode("UTF-8"))
    except Exception as e:
        logging.error(e)
        raise CoreError("Failed to start command: {}".format(command_line))