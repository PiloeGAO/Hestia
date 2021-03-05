"""
    :package:   Hestia
    :file:      kitsuWrapper.py
    :brief:     Kitsu wrapper class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os, logging
import gazu

from .defaultWrapper   import DefaultWrapper
from ....core.project   import Project
from ....core.category  import Category
from ....core.entity    import Entity
from ....core.version   import Version

class KitsuWrapper(DefaultWrapper):
    """Kitsu wrapper class.

    Args:
        manager (class: "Manager"): The Hestia Manager.
        api (str): Kitsu api address. Defaults to "".
    """
    def __init__(self, manager, api=""):
        super(KitsuWrapper, self).__init__()
        self.__manager = manager
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
            logging.error("API address is incorrect.")
            return False
        else:
            self.__active = True

        try:
            gazu.log_in(username, password)
        except gazu.exception.AuthFailedException:
            logging.info("Failed to login.")
            return False
        else:
            self._username = username + " (Online Mode: Kitsu)"
            return True
    
    def getOpenProjects(self):
        """Get open project.

        Returns:
            list: Projects datas.
        """
        logging.info("Getting users open projects.")
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
        logging.info("Getting datas for: %s" % project["name"])
        # Setting a temporary folder to save previews.
        tempPath = self.__manager.tempFolder

        # Get and create a new project.
        newProject = Project(id=project["id"], name=project["name"], description=project["description"])

        # Get, create and add categories to project.
        categories = gazu.asset.all_asset_types_for_project(project)

        for category in categories:
            newCategory = Category(id=category["id"], name=category["name"], description="", type="Assets")
            newProject.addCategory(newCategory)
        
        logging.info("Categories loaded.")

        # Get, create and add assets to categories.
        assets = gazu.asset.all_assets_for_project(project)

        for asset in assets:
            # Get all datas for asset.
            assetData = gazu.asset.get_asset(asset["id"])

            # Getting the preview picture.
            icon_path = ""
            try:
                preview_file = gazu.files.get_preview_file(assetData["preview_file_id"])
            except gazu.exception.NotAllowedException:
                logging.debug("%s : Acces refused to preview." % assetData["name"])
            else:
                if(preview_file["is_movie"]):
                    logging.debug("%s : Preview file is a movie, can't be loaded in Hestia." % assetData["name"])
                    icon_path = tempPath + os.path.sep + preview_file["id"] + ".png"
                    gazu.files.download_preview_file_thumbnail(preview_file, icon_path)
                else:
                    logging.debug("%s : Loading preview." % assetData["name"])
                    icon_path = tempPath + os.path.sep + preview_file["id"] + "." + preview_file["extension"]
                    gazu.files.download_preview_file(preview_file, icon_path)

            # Output versionning.
            versions = []
            outputs = gazu.files.all_output_files_for_entity(assetData)

            for output in outputs:
                task_type = gazu.task.get_task_type(output["task_type_id"])

                newVersion = Version(id=output["id"],
                                        name="%s: Revision %s" % (task_type["name"], output["revision"]),
                                        description="",
                                        workingPath=output["source_file"]["path"],
                                        outputPath=output["path"])

                versions.append(newVersion)

            # Buildint the Entity with all datas.
            newAsset = Entity(id=asset["id"],
                                name=asset["name"],
                                description=asset["description"],
                                icon=icon_path,
                                versions=versions)
            
            assetCategory = [category for category in newProject.categories if category.name == assetData["asset_type_name"]][0]
            assetCategory.addEntity(newAsset)
        
        
        logging.info("Assets loaded.")

        # Get, create and add sequences to project.
        sequences = gazu.shot.all_sequences_for_project(project)

        for sequence in sequences:
            newCategory = Category(id=sequence["id"],
                                    name=sequence["name"],
                                    description=sequence["description"],
                                    type="Shots")
            
            newProject.addCategory(newCategory)
        
        
        logging.info("Sequences loaded.")

        # Get, create and add shots to sequences.
        shots = gazu.shot.all_shots_for_project(project)

        for shot in shots:
            shotData = gazu.shot.get_shot(shot["id"])

            newShot = Entity(id=shot["id"],
                                name=shot["name"],
                                description=shot["description"],
                                icon="",
                                versions=[])

            shotSequence = [sequence for sequence in newProject.categories if sequence.name == shotData["sequence_name"]][0]
            shotSequence.addEntity(newShot)

        
        logging.info("Shots loaded.")

        return newProject