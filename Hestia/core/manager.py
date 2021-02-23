"""
    :package:   Hestia
    :file:      manager.py
    :brief:     Manager class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

from .links.kitsu.kitsuWrapper   import KitsuWrapper

from .project        import Project
from .category       import Category
from .entity         import Entity

class Manager():
    """Manager class.

    Args:
        currentManager (str): Manager name. Defaults to "kitsu".
        projects (list(class: "Project"), optional): Projects list. Defaults to [].
    """
    def __init__(self, currentManager= "kitsu", projects = [], **kwargs):
        self.__link = None

        self.__projects = projects

        if(currentManager == "kitsu"
            and kwargs["api"] != ""
            and kwargs["username"] != ""
            and kwargs["password"] != ""):
            self.__link = KitsuWrapper(api=kwargs["api"], username=kwargs["username"], password=kwargs["password"])
            self.__link.login()
        
        openProjects = self.__link.getOpenProjects()

        for project in openProjects:
            self.addProject(self.__link.getDatasFromProject(project))

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