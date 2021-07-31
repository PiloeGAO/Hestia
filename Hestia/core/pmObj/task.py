"""
    :package:   Hestia
    :file:      task.py
    :brief:     Task base class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
from .entity import Entity

class Task(Entity):
    """Task class.
    """
    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        pass