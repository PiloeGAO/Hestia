"""
    :package:   Hestia
    :file:      __init__.py
    :brief:     Root script of the USD submodule.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
from ..exceptions import CoreError

def check_usd_install():
    """Helper function to check if USD is available.
    """
    try:
        from pxr import Usd
        return True
    except ImportError:
        raise CoreError("Please add USD in your PYTHONPATH and PATH,\nthe procedure can be found here: https://graphics.pixar.com/usd/docs/USD-Tutorials.html")
    else:
        return False

def get_usd_extensions():
    """Get extensions associated to USD.
    
    Returns:
        list: str: Extensions.
    """
    return ["usd", "usda", "usdc"]