"""
    :package:   Hestia
    :file:      manager.py
    :brief:     Manager class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import logging

def get_logging(module_name, debug=True):
    """Get logging system for Hestia.

    Args:
        module_name (str): Name of the module to log.
        debug (bool, optional): Enable debug logging. Defaults to True.

    Returns:
        class:`logging`: Logger to be used.
    """
    logger = logging.getLogger(module_name)
    
    if(not logger.handlers):
        # If logger isn't setup, create one.
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter(
            "HESTIA | %(levelname)s - %(message)s @ [%(asctime)s] | %(pathname)s:%(lineno)d",
            "%y-%m-%d %H:%M:%S"
        )
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)
        if(debug):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.debug("Logging system setup successfully.")
    
    return logger