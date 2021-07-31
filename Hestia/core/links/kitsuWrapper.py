"""
    :package:   Hestia
    :file:      kitsuWrapper.py
    :brief:     Kitsu wrapper class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import os
import json
import gazu

from .defaultWrapper    import DefaultWrapper

from ..IO.path          import TemplateManager, FileManager

from ..pmObj.project    import Project
from ..pmObj.task       import Task
from ..pmObj.category   import Category
from ..pmObj.asset      import Asset
from ..pmObj.shot       import Shot
from ..pmObj.version    import Version
from ..pmObj.user       import User

class KitsuWrapper(DefaultWrapper):
    """Kitsu wrapper class.

    Args:
        api (str): Kitsu api address. Defaults to "".
    """
    def __init__(self, api="", *args, **kwargs):
        super(KitsuWrapper, self).__init__(*args, **kwargs)

        self._api            = api
        self._current_user   = None

        self._debug_kitsu_datas = False
    
    @property
    def api(self):
        """Get the api url.

        Returns:
            str: API URL.
        """
        return self._api
    
    @api.setter
    def api(self, api):
        """Set the api url.

        Args:
            api (str): API URL.
        """
        self._api = api

    def login(self, username="", password=""):
        """Login to Gazu.

        Returns:
            bool: State of the login.
        """

        try:
            gazu.client.set_host(self._api)
        except gazu.exception.HostException:
            self._manager.logging.error("API address is incorrect.")
            return False
        else:
            self._active = True

        try:
            gazu.log_in(username, password)
        except gazu.exception.AuthFailedException:
            self._manager.logging.info("Failed to login.")
            return False
        else:
            # Get, create and add users to wrapper.
            self._users = [
                User(id=user["id"], username=user["full_name"], email=user["email"], phone=user["phone"], role=user["role"], raw_datas=user)\
                for user in gazu.person.all_persons()
            ]

            self._current_user = [user for user in self._users if user.id == gazu.client.get_current_user()["id"]][0]
            self._username = self._current_user.username + " (Online Mode: Kitsu)"

            # Enable caching for faster download from online.
            gazu.cache.enable()

            return True
    
    def get_open_projects(self):
        """Get open project.

        Returns:
            list: Projects datas.
        """
        self._manager.logging.info("Getting users open projects.")
        if(self._active == False):
            return ConnectionError
        
        return gazu.project.all_open_projects()
    
    def get_datas_from_project(self, project):
        """Get data for the selected project.

        Args:
            project (str): Project datas.

        Returns:
            class: "Project": Project generated from kitsu.
        """
        self._manager.logging.info("Getting datas for: %s" % project["name"])

        # Setup project variables.
        description             = project["description"] if project["description"] != None else ""
        fps                     = project["fps"] if project["fps"] != None else 0
        ratio                   = project["ratio"] if project["ratio"] != None else 0
        resolution              = project["resolution"] if project["resolution"] != None else 0


        if(self._manager.debug and self._debug_kitsu_datas):
            self._manager.logging.debug("Project filetree: \n{}".format(json.dumps(project["file_tree"],\
                                            sort_keys=True, indent=4)))

        # Get and create a new project.
        new_project = Project(id=project["id"], name=project["name"], description=description,
                            fps=fps, ratio=ratio, resolution=resolution,
                            paths_template=self.convert_templates(project["file_tree"]),
                            raw_datas=project)

        if(self._manager.debug and self._debug_kitsu_datas):
            self._manager.logging.debug(json.dumps(project, sort_keys=True, indent=4))
        
        # Add users to project.
        new_project.team = [user for user in self._users if user.id in project["team"]]
        
        # Get, create and add tasks to project.
        tasks = gazu.task.all_task_types()

        for task in tasks:
            taskType = "Assets" if task["for_shots"] == "false" else "Shots"
            new_task = Task(taskType=taskType, id=task["id"], name=task["name"], raw_datas=task)
            new_project.add_task(new_task)

        if(self._manager.debug and self._debug_kitsu_datas):
            self._manager.logging.debug(json.dumps(tasks, sort_keys=True, indent=4))
        
        self._manager.logging.info("Tasks loaded.")

        # Get, create and add categories to project.
        categories = gazu.asset.all_asset_types_for_project(project)

        if(self._manager.debug and self._debug_kitsu_datas):
            self._manager.logging.debug(json.dumps(categories, sort_keys=True, indent=4))

        for category in categories:
            new_category = Category(id=category["id"], name=category["name"], description="", type="Assets", raw_datas=category)
            new_project.add_category(new_category)

            # Get, create and add assets to categories.
            assets = gazu.asset.all_assets_for_project_and_type(project, category)

            for asset in assets:
                
                if(self._manager.debug and self._debug_kitsu_datas):
                    self._manager.logging.debug(json.dumps(asset, sort_keys=True, indent=4))
                
                # Get tasks for asset.
                assetTasks = []
                for assetTask in gazu.task.all_task_types_for_asset(asset["id"]):
                    assetTasks.append([task for task in new_project.tasks if task.id == assetTask["id"]][0])
                
                # Output versionning.
                versions = self.get_versions(new_project, asset)

                # Buildint the Entity with all datas.
                newAsset = Asset(
                                    id=asset["id"],
                                    name=asset["name"],
                                    description=asset["description"],
                                    tasks=assetTasks,
                                    versions=versions,
                                    raw_datas=asset
                                )
                
                new_category.add_entity(newAsset)
            
        self._manager.logging.info("Categories and assets loaded.")

        # Get, create and add sequences to project.
        sequences = gazu.shot.all_sequences_for_project(project)

        if(self._manager.debug and self._debug_kitsu_datas):
            self._manager.logging.debug(json.dumps(sequences, sort_keys=True, indent=4))

        for sequence in sequences:
            newSequence = Category(id=sequence["id"],
                                    name=sequence["name"],
                                    description=sequence["description"],
                                    type="Shots",
                                    raw_datas=sequence)
            
            new_project.add_category(newSequence)

            # Get, create and add shots to sequences.
            shots = gazu.shot.all_shots_for_sequence(sequence)

            for shot in shots:

                if(self._manager.debug and self._debug_kitsu_datas):
                    self._manager.logging.debug(json.dumps(shot, sort_keys=True, indent=4))

                # Get technical datas.
                nb_frames = 0

                if(shot["nb_frames"] != None):
                    nb_frames = shot["nb_frames"]

                    if(nb_frames == 0 and 
                        shot["data"]["frame_in"] != None and shot["data"]["frame_out"] != None):
                        nb_frames = int(shot["data"]["frame_out"]) - int(shot["data"]["frame_in"])
                
                # Get Assets assigned in the shot.
                assigned_assets = [str(asset["id"]) for asset in gazu.asset.all_assets_for_shot(shot["id"])]

                # Get tasks for shot.
                shotTasks = []
                for shotTask in gazu.task.all_task_types_for_shot(shot["id"]):
                    shotTasks.append([task for task in new_project.tasks if task.id == shotTask["id"]][0])

                # Output versionning.
                versions = self.get_versions(new_project, shot)

                new_shot = Shot(
                                id=shot["id"],
                                name=shot["name"],
                                description=shot["description"],
                                tasks=shotTasks,
                                versions=versions,
                                frame_number=nb_frames,
                                assigned_assets=assigned_assets,
                                raw_datas=shot
                            )

                newSequence.add_entity(new_shot)

        self._manager.logging.info("Sequences and shots loaded.")

        return new_project

    def convert_templates(self, raw_datas={}):
        """Convert kitsu project path management to Hestia.
        
        Args:
            raw_datas (dict): Data from project request.
        
        Returns:
            dict: Path templates
        """
        temp_template = json.dumps(raw_datas)

        temp_template = temp_template.replace("<", "{")
        temp_template = temp_template.replace(">", "}")

        return json.loads(temp_template)
    
    def download_preview(self, entity=None):
        """Download the preview from Kitsu.

        Args:
            enitty (class:"Entity"): Entity. Defaults to None.

        Returns:
            str: Path of the icon.
        """
        if(int(self._manager.preferences.getValue("MANAGER", "loadPreviews")) == 0
            or entity == None):
            return ""
        
        entity_datas = gazu.entity.get_entity(entity.id)
        
        if(entity_datas["preview_file_id"] == None):
            return ""
        
        # Getting the preview picture.
        icon_path = ""
        tempPath = FileManager().temp_directory
        movies_exts = ["avi", "mov", "mkv", "mp4", "m4v"]

        try:
            preview_file = gazu.files.get_preview_file(entity_datas["preview_file_id"])
        except gazu.exception.NotAllowedException:
            self._manager.logging.debug("%s : Acces refused to preview." % entity_datas["name"])
        else:
            if(preview_file["extension"] in movies_exts and not bool(int(self._manager.preferences.getValue("MANAGER", "downloadVideos")))):
                self._manager.logging.debug("%s : Loading movie thumbnail." % entity_datas["name"])
                icon_path = tempPath + os.path.sep + preview_file["id"] + ".png"
                gazu.files.download_preview_file_thumbnail(preview_file, icon_path)
            else:
                self._manager.logging.debug("%s : Loading preview." % entity_datas["name"])
                icon_path = tempPath + os.path.sep + preview_file["id"] + "." + preview_file["extension"]
                gazu.files.download_preview_file(preview_file, icon_path)
        
        return icon_path
    
    def get_versions(self, project=None, entity=None):
        """Get versions for entity.

        Args:
            entityData (class:"gazu.entity", optional): Entity datas. Defaults to None.

        Returns:
            list:"Version": List of versions.
        """
        if(entity == None or project == None):
            return None

        versions = []
        outputs = gazu.files.all_output_files_for_entity(entity["id"])

        for output in outputs:
            task = [task for task in project.tasks if task.id == output["task_type_id"]][0]

            versions.append(
                Version(
                    id=output["id"],
                    name="",
                    description="",
                    task=task,
                    working_path=output["source_file"]["path"],
                    output_path=output["path"],
                    revision_number=output["revision"],
                    raw_datas=output)
            )

        return versions
    
    def publish(self, entity=None, name="", comment="", task_type_ID="", task_status="TODO", version="", software="", output_type="", working_file_path="", output_files=[], preview_file_path=""):
        """Publish files (working and outputs) to Kitsu. (Code from Guillaume Baratte project's called managerTools)

        Args:
            entity (class: `Entity`): Entity targeted.
            name (str, optional): Publish name. Defaults to "".
            comment (str, optional): Publish comment. Defaults to "".
            task_type_ID (str, optional): Tasktype ID. Defaults to "".
            task_status (str, optional): Status of the publish. Defaults to "TODO".
            version (str, optional): Version. Defaults to "".
            software (str, optional): Software name. Defaults to "".
            output_type (str, optional): Output type name. Defaults to "".
            working_file_path (str, optional): Working file path. Defaults to "".
            output_files (list, optional): Outputs files. Defaults to [].
            preview_file_path (str, optional): Preview image/video path. Defaults to "".

        Returns:
            bool: Publish status.
        """
        task = gazu.task.get_task_by_entity(entity.id, task_type_ID)

        # Add working file.
        working_file_data = {
            "name": name,
            "comment": comment,
            "person_id": self._current_user.id,
            "task_id": task["id"],
            "revision": version,
            "mode": "working"
        }

        # Assigning softwate.
        if(software != ""):
            software_data = gazu.client.fetch_first(
                            "softwares",
                            {
                                "name": name
                            })

            if(software_data != None):
                working_file_data["software_id"] = software_data["id"]
        
        # Create the working file entry on Zou.
        working_file_publish_data = gazu.client.post(
                                        "data/tasks/%s/working-files/new" % task["id"],
                                        working_file_data
                                    )
        
        # Set the path in the DB entry.
        gazu.client.put("data/working-files/%s" % working_file_publish_data["id"],
                {
                    "path": working_file_path
                }
            )

        # Add output files.
        output_files_publish_data = []
        for output_file_path in output_files:
            filename = os.path.split(output_file_path)[1]
            extension = os.path.splitext(output_file_path)[1]

            output_type_name = ""
            if(extension == ".ma"):
                output_type_name = "Maya Rig"
            elif(extension == ".abc" and entity.type == "Assets"):
                output_type_name = "ABC Modeling"
            elif(extension == ".abc" and entity.type == "Shots"):
                output_type_name = "ABC Animation"
            else:
                output_type_name = output_type

            output_type_data = gazu.client.fetch_first(
                                    "output-types",
                                    {
                                        "name": output_type_name
                                    }
                                )

            ouput_file_data = {
                "output_type_id": output_type_data["id"],
                "task_type_id": task["task_type_id"],
                "comment": comment,
                "revision": version,
                "representation": "output",
                "name": "%s_%s" % (name, filename),
                "nb_elements": 1,
                "sep": "/",
                "working_file_id": working_file_publish_data["id"],
                "person_id": self._current_user.id
            }
            
            outputFile_publish_data = gazu.client.post(
                                        "data/entities/%s/output-files/new" % task["entity_id"],
                                        ouput_file_data
                                        )
            
            gazu.client.put("data/output-files/%s" % outputFile_publish_data["id"],
                    {
                        "path" : output_file_path
                    }
                )
            
            output_files_publish_data.append(outputFile_publish_data)
        
        # Add the comment.
        task_status_data = gazu.task.get_task_status_by_short_name(task_status.lower())
        
        if(task_status_data != None):
            comment_data = {
                "task_status_id": task_status_data["id"],
                "comment": comment,
                "person_id": self._current_user.id
            }

            comment_publish_data = gazu.client.post('actions/tasks/%s/comment' % task["id"], comment_data)
        
            # Add the preview.
            preview_publish_data = gazu.client.post("actions/tasks/%s/comments/%s/add-preview" % (
                                    task["id"],
                                    comment_publish_data['id']
                                    ), {})

            gazu.client.upload(
                    'pictures/preview-files/%s' % preview_publish_data["id"],
                    preview_file_path
                )
                
            gazu.task.set_main_preview(preview_publish_data)
        else:
            self._manager.logging.error("Couldn't find the status for publishing, comment and preview wouldn't be published.")

        return True