"""
    :package:   Hestia
    :file:      kitsuWrapper.py
    :brief:     Kitsu wrapper class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
"""
import os, json
import gazu

from .defaultWrapper    import DefaultWrapper
from ....core.project   import Project
from ....core.task      import Task
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
        self.__api     = api
        self.__active  = False
        self._username = ""
        self.__userID  = ""

        self.__debugKitsuData = False

        self._loadPreviews = bool(int(self.__manager.preferences.getValue("MANAGER", "loadPreviews")))
    
    @property
    def api(self):
        """Get the api url.

        Returns:
            str: API URL.
        """
        return self.__api
    
    @api.setter
    def api(self, api):
        """Set the api url.

        Args:
            api (str): API URL.
        """
        self.__api = api

    def login(self, username="", password=""):
        """Login to Gazu.

        Returns:
            bool: State of the login.
        """

        try:
            gazu.client.set_host(self.__api)
        except gazu.exception.HostException:
            self.__manager.logging.error("API address is incorrect.")
            return False
        else:
            self.__active = True

        try:
            gazu.log_in(username, password)
        except gazu.exception.AuthFailedException:
            self.__manager.logging.info("Failed to login.")
            return False
        else:
            self._username = username + " (Online Mode: Kitsu)"
            self.__userID = gazu.client.get_current_user()["id"]

            # Enable caching for faster download from online.
            gazu.cache.enable()

            return True
    
    def getOpenProjects(self):
        """Get open project.

        Returns:
            list: Projects datas.
        """
        self.__manager.logging.info("Getting users open projects.")
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
        self.__manager.logging.info("Getting datas for: %s" % project["name"])

        # Setup project variables.
        description             = project["description"] if project["description"] != None else ""
        fps                     = project["fps"] if project["fps"] != None else 0
        ratio                   = project["ratio"] if project["ratio"] != None else 0
        resolution              = project["resolution"] if project["resolution"] != None else 0
        mountPoint              = project["file_tree"]["output"]["mountpoint"] if project["file_tree"] != None else ""
        rootPoint               = project["file_tree"]["output"]["root"] if project["file_tree"] != None else ""
        outputFilenameAsset     = project["file_tree"]["output"]["file_name"]["asset"] if project["file_tree"] != None else ""
        outputFilenameShot      = project["file_tree"]["output"]["file_name"]["shot"] if project["file_tree"] != None else ""
        outputFolderPathAsset   = project["file_tree"]["output"]["folder_path"]["asset"] if project["file_tree"] != None else ""
        outputFolderPathShot    = project["file_tree"]["output"]["folder_path"]["shot"] if project["file_tree"] != None else ""
        workingFilenameAsset    = project["file_tree"]["working"]["file_name"]["asset"] if project["file_tree"] != None else ""
        workingFilenameShot     = project["file_tree"]["working"]["file_name"]["shot"] if project["file_tree"] != None else ""
        workingFolderPathAsset  = project["file_tree"]["working"]["folder_path"]["asset"] if project["file_tree"] != None else ""
        workingFolderPathShot   = project["file_tree"]["working"]["folder_path"]["shot"] if project["file_tree"] != None else ""

        # Get and create a new project.
        newProject = Project(id=project["id"], name=project["name"], description=description,
                            fps=fps, ratio=ratio, resolution=resolution,
                            mountPoint=mountPoint,
                            rootPoint=rootPoint,
                            outputFilenameAsset=outputFilenameAsset,
                            outputFilenameShot=outputFilenameShot,
                            outputFolderPathAsset=outputFolderPathAsset,
                            outputFolderPathShot=outputFolderPathShot,
                            workingFilenameAsset=workingFilenameAsset,
                            workingFilenameShot=workingFilenameShot,
                            workingFolderPathAsset=workingFolderPathAsset,
                            workingFolderPathShot=workingFolderPathShot,
                            rawDatas=project)

        if(self.__manager.debug and self.__debugKitsuData):
            self.__manager.logging.debug(json.dumps(project, sort_keys=True, indent=4))
        
        # Get, create and add tasks to project.
        tasks = gazu.task.all_task_types()

        for task in tasks:
            taskType = "Assets" if task["for_shots"] == "false" else "Shots"
            newTask = Task(taskType=taskType, id=task["id"], name=task["name"], rawDatas=task)
            newProject.addTask(newTask)

        if(self.__manager.debug and self.__debugKitsuData):
            self.__manager.logging.debug(json.dumps(tasks, sort_keys=True, indent=4))
        
        self.__manager.logging.info("Tasks loaded.")

        # Get, create and add categories to project.
        categories = gazu.asset.all_asset_types_for_project(project)

        if(self.__manager.debug and self.__debugKitsuData):
            self.__manager.logging.debug(json.dumps(categories, sort_keys=True, indent=4))

        for category in categories:
            newCategory = Category(id=category["id"], name=category["name"], description="", type="Assets", rawDatas=category)
            newProject.addCategory(newCategory)

            # Get, create and add assets to categories.
            assets = gazu.asset.all_assets_for_project_and_type(project, category)

            for asset in assets:
                
                if(self.__manager.debug and self.__debugKitsuData):
                    self.__manager.logging.debug(json.dumps(asset, sort_keys=True, indent=4))
                
                # Get tasks for asset.
                assetTasks = []
                for assetTask in gazu.task.all_task_types_for_asset(asset["id"]):
                    assetTasks.append([task for task in newProject.tasks if task.id == assetTask["id"]][0])
                
                # Output versionning.
                versions = self.getVersions(newProject, asset)

                # Buildint the Entity with all datas.
                newAsset = Entity(manager=self.__manager,
                                    entityType="Assets",
                                    id=asset["id"],
                                    name=asset["name"],
                                    description=asset["description"],
                                    icon="",
                                    tasks=assetTasks,
                                    versions=versions,
                                    rawDatas=asset)
                
                newCategory.addEntity(newAsset)
            
        self.__manager.logging.info("Categories and assets loaded.")

        # Get, create and add sequences to project.
        sequences = gazu.shot.all_sequences_for_project(project)

        if(self.__manager.debug and self.__debugKitsuData):
            self.__manager.logging.debug(json.dumps(sequences, sort_keys=True, indent=4))

        for sequence in sequences:
            newSequence = Category(id=sequence["id"],
                                    name=sequence["name"],
                                    description=sequence["description"],
                                    type="Shots",
                                    rawDatas=sequence)
            
            newProject.addCategory(newSequence)

            # Get, create and add shots to sequences.
            shots = gazu.shot.all_shots_for_sequence(sequence)

            for shot in shots:

                if(self.__manager.debug and self.__debugKitsuData):
                    self.__manager.logging.debug(json.dumps(shot, sort_keys=True, indent=4))

                # Get technical datas.
                nb_frames = 0

                if(shot["nb_frames"] != None):
                    nb_frames = shot["nb_frames"]

                    if(nb_frames == 0 and 
                        shot["data"]["frame_in"] != None and shot["data"]["frame_out"] != None):
                        nb_frames = int(shot["data"]["frame_out"]) - int(shot["data"]["frame_in"])
                
                # Get Assets assigned in the shot.
                assignedAssets = [str(asset["id"]) for asset in gazu.asset.all_assets_for_shot(shot["id"])]

                # Get tasks for shot.
                shotTasks = []
                for shotTask in gazu.task.all_task_types_for_shot(shot["id"]):
                    shotTasks.append([task for task in newProject.tasks if task.id == shotTask["id"]][0])

                # Output versionning.
                versions = self.getVersions(newProject, shot)

                newShot = Entity(manager=self.__manager,
                                    entityType="Shots",
                                    id=shot["id"],
                                    name=shot["name"],
                                    description=shot["description"],
                                    icon="",
                                    tasks=shotTasks,
                                    versions=versions,
                                    frameNumber=nb_frames,
                                    assignedAssets=assignedAssets,
                                    rawDatas=shot)

                newSequence.addEntity(newShot)

        self.__manager.logging.info("Sequences and shots loaded.")

        return newProject
    
    def downloadPreview(self, entityType="Assets", entityId=None):
        """Download the preview from Kitsu.

        Args:
            entityData (class:"gazu.entity"): Entity datas. Defaults to None.

        Returns:
            str: Path of the icon.
        """
        if(int(self.__manager.preferences.getValue("MANAGER", "loadPreviews")) == 0):
            return ""
        
        if(entityType == "Assets"):
            entityData = gazu.asset.get_asset(entityId)
        elif(entityType == "Shots"):
            # Shots not supported for now (because "preview_file_id" is set to null in the DB).
            entityData = gazu.shot.get_shot(entityId)
        else:
            return ""
        
        if(entityData["preview_file_id"] == None):
            return ""
        
        # Getting the preview picture.
        icon_path = ""
        tempPath = self.__manager.tempFolder
        movies_exts = ["avi", "mov", "mkv", "mp4", "m4v"]

        try:
            preview_file = gazu.files.get_preview_file(entityData["preview_file_id"])
        except gazu.exception.NotAllowedException:
            self.__manager.logging.debug("%s : Acces refused to preview." % entityData["name"])
        else:
            if(preview_file["extension"] in movies_exts and not bool(int(self.__manager.preferences.getValue("MANAGER", "downloadVideos")))):
                self.__manager.logging.debug("%s : Loading movie thumbnail." % entityData["name"])
                icon_path = tempPath + os.path.sep + preview_file["id"] + ".png"
                gazu.files.download_preview_file_thumbnail(preview_file, icon_path)
            else:
                self.__manager.logging.debug("%s : Loading preview." % entityData["name"])
                icon_path = tempPath + os.path.sep + preview_file["id"] + "." + preview_file["extension"]
                gazu.files.download_preview_file(preview_file, icon_path)
        
        return icon_path
    
    def getVersions(self, project=None, entity=None):
        """Get versions for entity.

        Args:
            entityData (class:"gazu.entity", optional): Entity datas. Defaults to None.

        Returns:
            list:"Version": List of versions.
        """
        versions = []
        outputs = gazu.files.all_output_files_for_entity(entity["id"])

        for output in outputs:
            task = [task for task in project.tasks if task.id == output["task_type_id"]][0]

            newVersion = Version(id=output["id"],
                                    name="",
                                    description="",
                                    task=task,
                                    workingPath=output["source_file"]["path"],
                                    outputPath=output["path"],
                                    revisionNumber=output["revision"],
                                    rawDatas=output)

            versions.append(newVersion)

        return versions
    
    def publish(self, entity=None, name="", comment="", taskTypeID="", taskStatus="TODO", version="", software="", outputType="", workingFilePath="", outputFiles=[], previewFilePath=""):
        """Publish files (working and outputs) to Kitsu. (Code from Guillaume Baratte project's called managerTools)

        Args:
            entity (class: `Entity`): Entity targeted.
            name (str, optional): Publish name. Defaults to "".
            comment (str, optional): Publish comment. Defaults to "".
            taskTypeID (str, optional): Tasktype ID. Defaults to "".
            taskStatus (str, optional): Status of the publish. Defaults to "TODO".
            version (str, optional): Version. Defaults to "".
            software (str, optional): Software name. Defaults to "".
            outputType (str, optional): Output type name. Defaults to "".
            workingFilePath (str, optional): Working file path. Defaults to "".
            outputFiles (list, optional): Outputs files. Defaults to [].
            previewFilePath (str, optional): Preview image/video path. Defaults to "".

        Returns:
            bool: Publish status.
        """
        task = gazu.task.get_task_by_entity(entity.id, taskTypeID)

        # Add working file.
        workingFileData = {
            "name": name,
            "comment": comment,
            "person_id": self.__userID,
            "task_id": task["id"],
            "revision": version,
            "mode": "working"
        }

        # Assigning softwate.
        if(software != ""):
            softwareData = gazu.client.fetch_first(
                            "softwares",
                            {
                                "name": name
                            })

            if(softwareData != None):
                workingFileData["software_id"] = softwareData["id"]
        
        # Create the working file entry on Zou.
        workingFilePublishData = gazu.client.post(
                                        "data/tasks/%s/working-files/new" % task["id"],
                                        workingFileData
                                    )
        
        # Set the path in the DB entry.
        gazu.client.put("data/working-files/%s" % workingFilePublishData["id"],
                {
                    "path": workingFilePath
                }
            )

        # Add output files.
        outputFilesPublishData = []
        for outputFilePath in outputFiles:
            filename = os.path.split(outputFilePath)[1]
            extension = os.path.splitext(outputFilePath)[1]

            outputTypeName = ""
            if(extension == ".ma"):
                outputTypeName = "Maya Rig"
            elif(extension == ".abc" and entity.type == "Assets"):
                outputTypeName = "ABC Modeling"
            elif(extension == ".abc" and entity.type == "Shots"):
                outputTypeName = "ABC Animation"
            else:
                outputTypeName = outputType

            outputTypeData = gazu.client.fetch_first(
                                    "output-types",
                                    {
                                        "name": outputTypeName
                                    }
                                )

            ouputFileData = {
                "output_type_id": outputTypeData["id"],
                "task_type_id": task["task_type_id"],
                "comment": comment,
                "revision": version,
                "representation": "output",
                "name": "%s_%s" % (name, filename),
                "nb_elements": 1,
                "sep": "/",
                "working_file_id": workingFilePublishData["id"],
                "person_id": self.__userID
            }
            
            outputFilePublishData = gazu.client.post(
                                        "data/entities/%s/output-files/new" % task["entity_id"],
                                        ouputFileData
                                        )
            
            gazu.client.put("data/output-files/%s" % outputFilePublishData["id"],
                    {
                        "path" : outputFilePath
                    }
                )
            
            outputFilesPublishData.append(outputFilePublishData)
        
        # Add the comment.
        taskStatusData = gazu.task.get_task_status_by_short_name(taskStatus.lower())
        
        if(taskStatusData != None):
            commentData = {
                "task_status_id": taskStatusData["id"],
                "comment": comment,
                "person_id": self.__userID
            }

            commentPublishData = gazu.client.post('actions/tasks/%s/comment' % task["id"], commentData)
        
            # Add the preview.
            previewPublishData = gazu.client.post("actions/tasks/%s/comments/%s/add-preview" % (
                                    task["id"],
                                    commentPublishData['id']
                                    ), {})

            gazu.client.upload(
                    'pictures/preview-files/%s' % previewPublishData["id"],
                    previewFilePath
                )
                
            gazu.task.set_main_preview(previewPublishData)
        else:
            self.__manager.logging.error("Couldn't find the status for publishing, comment and preview wouldn't be published.")

        return True