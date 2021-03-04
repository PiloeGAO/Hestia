"""
    :package:   Hestia
    :file:      kitsuWrapper.py
    :brief:     Kitsu wrapper class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import gazu, json

from ..defaultWrapper   import DefaultWrapper
from ....core.project   import Project
from ....core.category  import Category
from ....core.entity    import Entity

class KitsuWrapper(DefaultWrapper):
    def __init__(self, api=""):
        super(KitsuWrapper, self).__init__()
        self.__api      = api
        self.__active   = False
        self._username = ""

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
            self._username = username + " (Online Mode: Kitsu)"
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
        newProject = Project(id=project["id"], name=project["name"], description=project["description"])

        # Get, create and add categories to project.
        categories = gazu.asset.all_asset_types_for_project(project)

        for category in categories:
            newCategory = Category(id=category["id"], name=category["name"], description="", type="Assets")
            newProject.addCategory(newCategory)
        
        # Get, create and add assets to categories.
        assets = gazu.asset.all_assets_for_project(project)

        for asset in assets:
            # Get all datas for asset.
            assetData = gazu.asset.get_asset(asset["id"])

            # TODO: Make a proper implementation of thumbnail download.
            # Download the preview picture.
            # path = "/datas/" + assetData["preview_file_id"] + ".png"
            # gazu.files.download_preview_file_thumbnail(assetData["preview_file_id"], path)

            # TODO: Get tasks and versions to build local versioning system.
            versions = []
            outputs = gazu.files.all_output_files_for_entity(assetData)

            for output in outputs:
                task_type = gazu.task.get_task_type(output["task_type_id"])
                versions.append("%s: Revision %s" % (task_type["name"], output["revision"]))

            newAsset = Entity(id=asset["id"],
                                name=asset["name"],
                                description=asset["description"],
                                path="",
                                icon="",
                                versions=versions)
            
            assetCategory = [category for category in newProject.categories if category.name == assetData["asset_type_name"]][0]
            assetCategory.addEntity(newAsset)
        
        # Get, create and add sequences to project.
        sequences = gazu.shot.all_sequences_for_project(project)

        for sequence in sequences:
            newCategory = Category(id=sequence["id"],
                                    name=sequence["name"],
                                    description=sequence["description"],
                                    type="Shots")
            
            newProject.addCategory(newCategory)
        
        # Get, create and add shots to sequences.
        shots = gazu.shot.all_shots_for_project(project)

        for shot in shots:
            shotData = gazu.shot.get_shot(shot["id"])

            newShot = Entity(id=shot["id"],
                                name=shot["name"],
                                description=shot["description"],
                                path="",
                                icon="",
                                versions=[])

            shotSequence = [sequence for sequence in newProject.categories if sequence.name == shotData["sequence_name"]][0]
            shotSequence.addEntity(newShot)

        return newProject