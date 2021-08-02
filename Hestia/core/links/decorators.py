"""
    :package:   Hestia
    :file:      decorators.py
    :brief:     Links decorators.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import functools

def sync_entity(func):
    """Decorator to load entities dynamicly.
    
    Args:
        func (function): Function to execute.
    
    Returns:
        function: Function to execute.
    """
    @functools.wraps(func)
    def wrapper_sync_entity(*args, **kwargs):
        current_obj = args[0]

        if(not current_obj.is_downloaded):
            current_obj.is_downloaded = True
            
            from ..manager import current_manager

            from ..pmObj.asset    import Asset
            from ..pmObj.category import Category
            from ..pmObj.shot     import Shot
            from ..pmObj.task     import Task
            from ..pmObj.version  import Version

            if(isinstance(current_obj, Asset)):
                current_manager().link.get_datas_for_asset(current_obj)
            elif(isinstance(current_obj, Category)):
                current_manager().link.get_datas_for_category(current_obj)
            elif(isinstance(current_obj, Shot)):
                current_manager().link.get_datas_for_shot(current_obj)
            elif(isinstance(current_obj, Task)):
                current_manager().link.get_datas_for_task(current_obj)
            elif(isinstance(current_obj, Version)):
                current_manager().link.get_datas_for_version(current_obj)

        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_sync_entity