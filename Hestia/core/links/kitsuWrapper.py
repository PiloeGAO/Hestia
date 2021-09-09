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

from ..IO.path          import TemplateManager, FileManager, remove_special_characters

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

        self._name = "KITSU"

        self._api                       = api
        self._current_user              = None

        self._setup_kitsu_for_hestia    = kwargs.get("setup_kitsu", False)

        self._debug_kitsu_datas         = False

        if(bool(os.environ.get("HESTIA_AUTOLOGIN", False))):
            self._manager.logging.info("Using auto-logging to Kitsu.")
            self._manager.projects = []

            self._api = os.environ.get("HESTIA_API","http://localhost:80/api")
            self.login(username=os.environ.get("HESTIA_LOGIN","username"), password=os.environ.get("HESTIA_PASSWORD","password"))

            openProjects = self.get_open_projects()

            for project in openProjects:
                self._manager.addProject(self.get_datas_from_project(project))
    
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
            self._users = []

            current_user_raw_datas = gazu.client.get_current_user()

            self._current_user = User(id=current_user_raw_datas["id"],
                                    username=current_user_raw_datas["full_name"],
                                    email=current_user_raw_datas["email"],
                                    phone=current_user_raw_datas["phone"],
                                    role=current_user_raw_datas["role"],
                                    raw_datas=current_user_raw_datas
                                )

            self._users.append(self._current_user)

            self._username = self._current_user.username + " (Online Mode: Kitsu)"

            if(self._current_user.role == "admin" and self._setup_kitsu_for_hestia):
                self.setup_output_filetypes()

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
    
    def get_datas_from_project(self, raw_datas):
        """Get data for the selected project.

        Args:
            raw_datas (str): Project raw datas.

        Returns:
            class: "Project": Project generated from kitsu.
        """
        self._manager.logging.info("Getting datas for: %s" % raw_datas["name"])

        # Setup project variables.
        description             = raw_datas["description"] if raw_datas["description"] != None else ""
        fps                     = raw_datas["fps"] if raw_datas["fps"] != None else 0
        ratio                   = raw_datas["ratio"] if raw_datas["ratio"] != None else 0
        resolution              = raw_datas["resolution"] if raw_datas["resolution"] != None else 0

        # Get and create a new project.
        new_project = Project(id=raw_datas["id"], name=raw_datas["name"], description=description,
                            fps=fps, ratio=ratio, resolution=resolution,
                            paths_template=self.convert_templates(raw_datas["file_tree"]),
                            raw_datas=raw_datas)
        
        # Get, create and add users to wrapper.
        for user_id in [user_id for user_id in raw_datas["team"] if user_id not in [user.id for user in self._users]]:
            user_raw_datas = gazu.person.get_person(user_id)
            self._users.append(
                User(id=user_raw_datas["id"],
                    username=user_raw_datas["full_name"],
                    email=user_raw_datas["email"],
                    phone=user_raw_datas["phone"],
                    role=user_raw_datas["role"],
                    raw_datas=user_raw_datas
                )
            )

        new_project.team = [user for user in self._users if user.id in raw_datas["team"]]
        
        # Get, create and add tasks to project.
        tasks = gazu.task.all_task_types()

        for task in tasks:
            taskType = "Assets" if task["for_shots"] == "false" else "Shots"
            new_task = Task(taskType=taskType, id=task["id"], name=task["name"], raw_datas=task)
            new_project.add_task(new_task)
        
        self._manager.logging.info("Tasks loaded.")

        # Get, create and add categories to project.
        categories = gazu.asset.all_asset_types_for_project(raw_datas)

        for category in categories:
            new_category = Category(id=category["id"], name=category["name"], description="", type="Assets", raw_datas=category)
            new_project.add_category(new_category)
            
        self._manager.logging.info("Categories and assets loaded.")

        # Get, create and add sequences to project.
        sequences = gazu.shot.all_sequences_for_project(raw_datas)

        for sequence in sequences:
            newSequence = Category(id=sequence["id"],
                                    name=sequence["name"],
                                    description=sequence["description"],
                                    type="Shots",
                                    raw_datas=sequence)
            
            new_project.add_category(newSequence)

        self._manager.logging.info("Sequences and shots loaded.")

        return new_project


    def get_datas_for_asset(self, asset):
        """Get data for the given asset.
        
        Args:
            asset (class:`Asset`): Asset to dowload.
        
        Returns:
            class:`Asset`: Asset.
        """
        raw_datas = gazu.asset.get_asset(asset.id)

        asset.name = raw_datas["name"]
        asset.description = raw_datas["description"]

        asset.preview_file = self.download_preview(asset)

        for task in raw_datas["tasks"]:
            Task(id=task["id"])

        asset.versions = self.get_versions(self._manager.get_current_project(), raw_datas)

        # Build the path to asset master USD.
        template_path = TemplateManager().get_template_path_for_entity(self._manager.get_current_project().paths_template, publish=True, parent_entity="asset", target_entity="Asset")

        current_category = [category for category in self._manager.get_current_project().categories if asset.id in [entity.id for entity in category.entities]][0]
        asset.path = os.path.join(
                        TemplateManager().get_folderpath_from_template(
                            template=template_path,
                            project=self._manager.get_current_project(),
                            category=current_category,
                            entity=asset
                        ),
                        "{}.usda".format(remove_special_characters(asset.name))
                    )

        asset.raw_datas = raw_datas

        return asset

    def get_datas_for_category(self, category):
        """Get data for the given category.
        
        Args:
            category (class:`Category`): Category to download.
        
        Returns:
            class:`Category`: Category.
        """
        if(category.type == "Assets"):
            raw_datas = gazu.asset.all_assets_for_project_and_type(self._manager.get_current_project().id, category.id)

            for asset in raw_datas:
                category.add_entity(Asset(id=asset["id"]))

        else:
            raw_datas = gazu.shot.all_shots_for_sequence(category.id)

            for shot in raw_datas:
                category.add_entity(Shot(id=shot["id"]))

        return category

    def get_datas_for_shot(self, shot):
        """Get data for the given shot.
        
        Args:
            shot (class:`Shot`): Shot to download.
        
        Returns:
            class:`Shot`: Shot.
        """
        raw_datas = gazu.shot.get_shot(shot.id)

        shot.name = raw_datas["name"]
        shot.description = raw_datas["description"]

        shot.preview_file = self.download_preview(shot)

        if(raw_datas.get("nb_frames") != None
            or raw_datas.get("frame_in") != None
            or raw_datas.get("frame_out") != None):
            # This case is needed in case of no frame duration entered in the DB.
            if(raw_datas.get("nb_frames", 0) > 0):
                shot.frame_number = int(raw_datas.get("nb_frames", 0))
            else:
                shot.frame_number = int(raw_datas.get("frame_out", 0)) - int(raw_datas.get("frame_in", 0)) + 1

        shot.versions = self.get_versions(self._manager.get_current_project(), raw_datas)

        shot.assigned_assets = [str(asset["id"]) for asset in gazu.asset.all_assets_for_shot(raw_datas["id"])]

        # Build the path to shot master USD.
        template_path = TemplateManager().get_template_path_for_entity(self._manager.get_current_project().paths_template, publish=True, parent_entity="shot", target_entity="Shot")

        current_category = [category for category in self._manager.get_current_project().categories if shot.id in [entity.id for entity in category.entities]][0]
        shot.path = os.path.join(
                        TemplateManager().get_folderpath_from_template(
                            template=template_path,
                            project=self._manager.get_current_project(),
                            category=current_category,
                            entity=shot
                        ),
                        "{}.usda".format(remove_special_characters(shot.name))
                    )

        shot.raw_datas = raw_datas
        
        return shot

    def get_datas_for_task(self, task):
        """Get data for the given task.
        
        Args:
            task (class:`Task`): Task to download.
        
        Returns:
            class:`Task`: Task.
        """
        # No need to use the defered loading for tasks,
        # the main request already get all datas.
        return task

    def get_datas_for_version(self, version):
        """Get data for the given version.
        
        Args:
            version (class:`Version`): Version to download.
        
        Returns:
            class:`Version`: Version.
        """
        # Not used for Kitsu (Kitsu use a different way to get versions).
        # This can be used for REST requests later.
        return version

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
        target_path = ""

        try:
            preview_file = gazu.files.get_preview_file(entity_datas["preview_file_id"])
        except gazu.exception.NotAllowedException:
            self._manager.logging.debug("%s : Acces refused to preview." % entity_datas["name"])
        else:
            self._manager.logging.debug("%s : Downloading thumbnail." % entity_datas["name"])
            target_path = os.path.join(FileManager().temp_directory, preview_file["id"] + ".png")
            gazu.files.download_preview_file_thumbnail(preview_file, target_path)
        
        return target_path
    
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
    
    def setup_output_filetypes(self):
        """Setup output filetypes.
        """
        filetypes = [
            # Major DCCs.
            {"name":"Blender Scene",            "short_name":"blend"},
            {"name":"Maya ASCII Scene",         "short_name":"ma"},
            {"name":"Maya Binary Scene",        "short_name":"mb"},
            {"name":"Houdini Apprentice Scene", "short_name":"hipnc"},
            {"name":"Houdini Indie Scene",      "short_name":"hiplc"},
            {"name":"Houdini FX Scene",         "short_name":"hip"},
            {"name":"Nuke Script",              "short_name":"nk"},
            # Major CGI formats.
            {"name":"USD ASCII Stage",          "short_name":"usda"},
            {"name":"USD Binary Stage",         "short_name":"usd"},
            {"name":"Alembic File",             "short_name":"abc"},
            {"name":"Volume File",              "short_name":"vdb"},
            {"name":"Material X",               "short_name":"mtlx"},
            {"name":"OSL Shader",               "short_name":"osl"},
            # Image formats.
            {"name":"PNG",                      "short_name":"png"},
            {"name":"EXR",                      "short_name":"exr"},
            {"name":"JPG",                      "short_name":"jpg"},
            {"name":"JPEG",                     "short_name":"jpeg"},
            {"name":"HDR",                      "short_name":"hdr"},
            {"name":"TX",                       "short_name":"tx"},
            # Movie formats.
        ]

        for filetype in filetypes:
            gazu.files.new_output_type(filetype["name"], filetype["short_name"])

    def publish(self, entity=None, name="", comment="", task_type_ID="", task_status="TODO", version="",\
        software="", output_type="", working_file_path="", output_files=[], preview_file_path=""):
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

        if(not task):
            self._manager.logging.error(
                "Publish cannot be done for task ID {}.".format(task_type_ID)
            )
            return False

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
            extension = os.path.splitext(output_file_path)[1][1:]

            output_type_name = None

            for output_filetype in gazu.files.all_output_types():
                if(extension.lower() == output_filetype["short_name"].lower()):
                    output_type_name = output_filetype["name"]

            if(output_type_name == None):
                self._manager.logging.error(
                    "Publish cannot be done for {} due to missing output filetype in Kitsu.".format(filename)
                )
                continue

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