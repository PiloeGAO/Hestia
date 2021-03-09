"""
    :package:   Hestia
    :file:      manager.py
    :brief:     Manager class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import shutil, logging
import tempfile, atexit

from .links.dccs.defaultIntegration         import DefaultIntegration

from .links.projectManagers.defaultWrapper  import DefaultWrapper
from .links.projectManagers.kitsuWrapper    import KitsuWrapper

from .project                               import Project

class Manager():
    """Manager class.

    Args:
        projects (list(class: "Project"), optional): Projects list. Defaults to [].
    """
    def __init__(self, integration = "standalone", projects = [Project(name="local", description="Local file system.")], **kwargs):
        # Setting up the logging display.
        logging.basicConfig(format="HESTIA | %(levelname)s @ %(asctime)s | %(message)s")

        self.__version  = "0.0.1"
        self.__debugMode    = True

        # Initialize the custom logging system.
        self.__logging = None
        self.initializeLogging()

        # Managing integrations.
        if(integration == "Maya"):
            from .links.dccs.mayaIntegration import MayaIntegration
            self.__integration = MayaIntegration(manager=self)
        else:
            self.__integration = DefaultIntegration()

        # 
        self.__tempFolder = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, self.__tempFolder)
        
        self.__link = DefaultWrapper()

        self.__projects = projects
        self.__currentProject = 0
    
    @property
    def logging(self):
        """Get the custom logging system.

        Returns:
            class: "logging": Logging system.
        """
        return self.__logging
    
    @property
    def integration(self):
        """Get the current integration used.

        Returns:
            class: "DefaultIntegration" : Get the integration class to communicate with the DCC.
        """
        return self.__integration

    @property
    def tempFolder(self):
        """Get the temporary folder of this instance.

        Returns:
            str: Folder Path.
        """
        return self.__tempFolder

    @property
    def projects(self):
        """Get all projects stored in the manager.

        Returns:
            list(class: "Project"): Projects list.
        """
        return self.__projects
    
    @projects.setter
    def projects(self, projects):
        """Override the projects list.

        Args:
            projects (list(class: "Project")): Projects list.
        """
        self.__projects = projects
    
    @property
    def currentProject(self):
        """Get the current project.

        Returns:
            int: Project ID.
        """
        return self.__currentProject
    
    @currentProject.setter
    def currentProject(self, newCurrentProject):
        """Set the current project.

        Args:
            newCurrentProject (int): New current project.
        """
        if(newCurrentProject is int):
            self.__currentProject = newCurrentProject
        else:
            self.__currentProject = 0
    
    @property
    def link(self):
        """Get the current link.

        Returns:
            class: "KitsuWrapper": Current link.
        """
        return self.__link
    
    @property
    def version(self):
        """Get the manager version.

        Returns:
            str: Manager version.
        """
        return self.__version
    
    def initializeLogging(self):
        """Setup the logging system.
        """
        self.__logging = logging.getLogger(__name__)
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter("HESTIA | %(levelname)s @ %(asctime)s | %(message)s")
        streamHandler.setFormatter(formatter)
        self.__logging.addHandler(streamHandler)
        if(self.__debugMode):
            self.__logging.setLevel(logging.DEBUG)
        else:
            self.__logging.setLevel(logging.INFO)

        self.__logging.debug("Logging system setup successfully.")

    
    def addProject(self, project):
        """Add a new project to the projects list.

        Args:
            project (class: "Project"): New project to add.
        """
        self.__projects.append(project)
    
    def removeProject(self, projectName):
        """Remove a project for the projects list.

        Args:
            projectName (class: "Project"): Project to remove.
        """
        #TODO: MOVE TO COMPREHENSIVE LIST.
        for project in self.__projects:
            if(project.name == projectName):
                del project
    
    def connectToOnline(self, cleanProjects=True, service="kitsu", **kwargs):
        """Connect manager to an online service.

        Args:
            service (str, optional): Service name. Defaults to "kitsu".

        Returns:
            bool: Connection status.
        """
        if(cleanProjects):
            self.__projects = []

        if(service == "kitsu"
            and kwargs["api"] != ""
            and kwargs["username"] != ""
            and kwargs["password"] != ""):
            self.__link = KitsuWrapper(manager=self, api=kwargs["api"])
            isUserLoged = self.__link.login(username=kwargs["username"], password=kwargs["password"])

            if(isUserLoged):
                openProjects = self.__link.getOpenProjects()

                for project in openProjects:
                    self.addProject(self.__link.getDatasFromProject(project))
                
                return True

            return False
        return False