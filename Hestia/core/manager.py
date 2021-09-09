"""
    :package:   Hestia
    :file:      manager.py
    :brief:     Manager class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import sys
import os
import shutil
import tempfile
import atexit
import traceback

from .logger    import get_logging, shutdown_logger
logger = get_logging(debug = bool(os.environ.get("DEBUG", "False")))

from .exceptions    import CoreError
from .IO.path   import FileManager
from .preferences   import Preferences

from .USD   import check_usd_install

from .pmObj.project import Project


class Manager():
    """Manager class.
    """
    def __init__(self, integration="standalone", **kwargs):
        # Set Manager version.
        self._version  = "0.0.5Dev"

        # Loading preferences.
        self._preferences = Preferences(manager=self)
        isPreferencesLoaded = self._preferences.loadPreferences()

        if(not isPreferencesLoaded):
            # Saving blank preferences on install
            self._preferences.generatePreferences()
            self._preferences.savePreferences()

        # Setup custom exception handling.
        sys.excepthook = self.custom_except_hook

        # Check if USD library is available.
        check_usd_install() 

        # Setup projects.
        self._projects = [Project(name="local", description="Local file system.", is_downloaded=True)]
        self._current_project = 0

        # Managing integrations.
        if(integration == "Maya"):
            from Hestia.core.dccs.maya import MayaIntegration
            self._integration = MayaIntegration(manager=self)
        else:
            from Hestia.core.dccs.default import DefaultIntegration
            self._integration = DefaultIntegration()
        
        # Setting up the service.
        if(self._preferences.getValue("MANAGER", "service") == "kitsu"):
            from .links.kitsuWrapper import KitsuWrapper
            self._mode = "kitsu"
            self._link = KitsuWrapper(manager=self, api=self._preferences.getValue("MANAGER", "onlineHost"))
        else:
            from .links.defaultWrapper import DefaultWrapper
            self._mode = "local"
            self._link = DefaultWrapper()

        atexit.register(self.close_manager)
    
    @property
    def logging(self):
        """Get the custom logging system.

        Returns:
            class: "logging": Logging system.
        """
        return logger
    
    @property
    def debug(self):
        """Get the current state of debug of the manager.

        Returns:
            bool: Debug state.
        """
        return self._debugMode
    
    @property
    def integration(self):
        """Get the current integration used.

        Returns:
            class: "DefaultIntegration" : Get the integration class to communicate with the DCC.
        """
        return self._integration

    @property
    def projects(self):
        """Get all projects stored in the manager.

        Returns:
            list(class: "Project"): Projects list.
        """
        return self._projects
    
    @projects.setter
    def projects(self, projects):
        """Override the projects list.

        Args:
            projects (list(class: "Project")): Projects list.
        """
        self._projects = projects
    
    @property
    def current_project(self):
        """Get the current project.

        Returns:
            int: Project ID.
        """
        return self._current_project
    
    @current_project.setter
    def current_project(self, new_current_project):
        """Set the current project.

        Args:
            newcurrent_project (int): New current project.
        """
        if(new_current_project is int):
            self._current_project = new_current_project
        else:
            self._current_project = 0

    def get_current_project(self):
        """Get the current project (Hestia object).
        
        Returns:
            class:`Project`: Current project.
        """
        return self._projects[self._current_project]
    
    @property
    def link(self):
        """Get the current link.

        Returns:
            class: "KitsuWrapper": Current link.
        """
        return self._link
    
    @property
    def mode(self):
        """Get the current mode.

        Returns:
            str: Current link mode.
        """
        return self._mode

    @property
    def preferences(self):
        """Get the preference manager.

        Returns:
            class: 'Preferences' : Preference class.
        """
        return self._preferences

    @property
    def version(self):
        """Get the manager version.

        Returns:
            str: Manager version.
        """
        return self._version
    
    def addProject(self, project):
        """Add a new project to the projects list.

        Args:
            project (class: "Project"): New project to add.
        """
        self._projects.append(project)
    
    def removeProject(self, projectName):
        """Remove a project for the projects list.

        Args:
            projectName (class: "Project"): Project to remove.
        """
        #TODO: MOVE TO COMPREHENSIVE LIST.
        for project in self._projects:
            if(project.name == projectName):
                del project
    
    def connectToOnline(self, cleanProjects=True, **kwargs):
        """Connect manager to an online service.

        Args:
            service (str, optional): Service name. Defaults to "kitsu".

        Returns:
            bool: Connection status.
        """
        if(cleanProjects):
            self._projects = []

        if(self._mode == "kitsu"
            and kwargs["api"] != ""
            and kwargs["username"] != ""
            and kwargs["password"] != ""):
            self._link.api = kwargs["api"]
            isUserLoged = self._link.login(username=kwargs["username"], password=kwargs["password"])

            if(isUserLoged):
                openProjects = self._link.get_open_projects()

                for project in openProjects:
                    self.addProject(self._link.get_datas_from_project(project))
                
                return True

            return False
        return False

    def close_manager(self):
        """Function to exec before close handlers.
        """
        self._preferences.savePreferences()
        shutdown_logger()
        shutil.rmtree(FileManager().temp_directory)

    def custom_except_hook(self, exc_type, exc_val, tb):
        """Original function: https://docs.python.org/3/library/sys.html#sys.excepthook
        """
        # Display crash informations.
        tb = '\n'.join([''.join(traceback.format_tb(tb)),
                        '{0}: {1}'.format(exc_type.__name__, exc_val)])
        logger.critical('unhandled exception:\n{}'.format(tb))

        # Copy temp directory to zip archive in user home(needed for debug).
        FileManager().copy_file(os.path.join(os.path.expanduser("~"), ".hestia.config"), FileManager().temp_directory)
        shutil.make_archive(os.path.join(os.path.expanduser('~'), "hestia_crash_report"), "zip", FileManager().temp_directory)

#################################################################################
# Manager management
#################################################################################
CURRENT_MANAGER = None

def set_current_manager(manager):
    """Set the current manager.

    Args:
        manager (class:`Manager`): Manager instance.
    """
    global CURRENT_MANAGER
    CURRENT_MANAGER = manager

def current_manager():
    """Get current manager.

    Returns:
        class:`Manager`: Manager instance.
    """
    global CURRENT_MANAGER
    return CURRENT_MANAGER

def start_manager(*args, **kwargs):
    """Start a manager.

    Raises:
        RuntimeError: Manager already started.

    Returns:
        class:`Manager`: Manager initialized.
    """
    if(current_manager()):
        raise CoreError("Manager already started.")
    
    integration = kwargs["integration"] if "integration" in kwargs  else "standalone"

    manager = Manager(integration)
    set_current_manager(manager)

    return manager