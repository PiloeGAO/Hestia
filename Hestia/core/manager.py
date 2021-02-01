"""
    :package:   Hestia
    :file:      manager.py
    :brief:     Manager class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

from Hestia.core.project import Project

class Manager():
    """Manager class.

    Args:
        projects (list(class: "Project"), optional): Projects list. Defaults to [].
    """
    def __init__(self, projects = []):
        self.__projectsList = projects

    @property
    def projectsList(self):
        """Get all projects stored in the manager.

        Returns:
            list(class: "Project"): Projects list.
        """
        return self.__projectsList
    
    @projectsList.setter
    def projectsList(self, projects):
        """Override the projects list.

        Args:
            projects (list(class: "Project")): Projects list.
        """
        self.__projectsList = projects
    
    def addProject(self, project):
        """Add a new project to the projects list.

        Args:
            project (class: "Project"): New project to add.
        """
        self.__projectsList.append(project)
    
    def removeProject(self, projectName):
        """Remove a project for the projects list.

        Args:
            projectName (class: "Project"): Project to remove.
        """
        for project in self.__projectsList:
            if(project.name == projectName):
                del project