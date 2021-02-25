"""
    :package:   Hestia
    :file:      kitsuWrapper.py
    :brief:     Kitsu wrapper class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

import gazu

from ..defaultWrapper   import DefaultWrapper
from ....core.project   import Project
from ....core.category  import Category
from ....core.entity    import Entity

class KitsuWrapper(DefaultWrapper):
    def __init__(self, api=""):
        super(KitsuWrapper, self).__init__()
        self.__api      = api
        self.__active   = False

    def login(self, username="", password=""):
        """Login to Gazu.

        Returns:
            bool: State of the login.
        """

        try:
            gazu.client.set_host(self.__api)
        except gazu.exception.HostException:
            return False
        else:
            self.__active = True

        try:
            gazu.log_in(username, password)
        except gazu.exception.AuthFailedException:
            return False
        else:
            self.__username = username
            return True
    
    def getOpenProjects(self):
        """Get open project.

        Returns:
            list: Projects datas.
        """
        if(self.__active == False):
            return ConnectionError
        
        return gazu.project.all_open_projects()
    
    def getDatasFromProject(self, project):
        """Get data for the selected project.

        Args:
            project (str): Project datas.

        Returns:
            class: "Project": Project generated from kitsu.
        """
        # Get and create a new project.
        newProject = Project(project["name"], project["description"])

        # Get, create and add categories to project.
        categories = gazu.asset.all_asset_types_for_project(project)

        for category in categories:
            newCategory = Category(name=category["name"], description="", type="Asset")
            newProject.addCategory(newCategory)
        
        # Get, create ad add assets to categories.
        assets = gazu.asset.all_assets_for_project(project)

        for asset in assets:
            # Get all datas for asset.
            assetData = gazu.asset.get_asset(asset["id"])

            # TODO: Make a proper implementation of thumbnail download.
            # Download the preview picture.
            # path = "/datas/" + assetData["preview_file_id"] + ".png"
            # gazu.files.download_preview_file_thumbnail(assetData["preview_file_id"], path)

            newAsset = Entity(name=asset["name"],
                                description=asset["description"],
                                path="",
                                icon="",
                                versions=[])
            
            assetCategory = [category for category in newProject.categories if category.name == assetData["asset_type_name"]][0]
            assetCategory.addEntity(newAsset)
        
        # TODO: Import Shots.

        return newProject