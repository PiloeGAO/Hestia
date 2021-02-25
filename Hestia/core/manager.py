"""
    :package:   Hestia
    :file:      manager.py
    :brief:     Manager class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

from .links.defaultWrapper      import DefaultWrapper
from .links.kitsu.kitsuWrapper  import KitsuWrapper

class Manager():
    """Manager class.

    Args:
        currentManager (str): Manager name. Defaults to "kitsu".
        projects (list(class: "Project"), optional): Projects list. Defaults to [].
    """
    def __init__(self, projects = [], **kwargs):
        self.__version = "0.0.1"

        self.__link = DefaultWrapper()

        self.__projects = projects

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
    
    def connectToOnline(self, service="kitsu", **kwargs):
        """Connect manager to an online service.

        Args:
            service (str, optional): Service name. Defaults to "kitsu".

        Returns:
            bool: Connection status.
        """
        #TODO: OPTIMIZE THIS FUNCTION.
        if(service == "kitsu"
            and kwargs["api"] != ""
            and kwargs["username"] != ""
            and kwargs["password"] != ""):
            self.__link = KitsuWrapper(api=kwargs["api"])
            isUserLoged = self.__link.login(username=kwargs["username"], password=kwargs["password"])
        else:
            return False
        
        if(isUserLoged):
            openProjects = self.__link.getOpenProjects()

            for project in openProjects:
                self.addProject(self.__link.getDatasFromProject(project))
            
            return True
        else:
            return False