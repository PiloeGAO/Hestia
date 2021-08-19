"""
    :package:   Hestia
    :file:      __init__.py
    :brief:     Root script of the USD submodule.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
from ..exceptions import CoreError

try:
    from pxr import Usd
except ImportError:
    raise CoreError("Please add USD in your PYTHONPATH and PATH,\nthe procedure can be found here: https://graphics.pixar.com/usd/docs/USD-Tutorials.html")