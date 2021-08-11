"""
    :package:   Hestia
    :file:      path.py
    :brief:     path functions.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import os
import shutil
import tempfile

from ..exceptions import CoreError

SPECIALCHARACTERSLIST = [" ", "-", "'", "\"", "`", "^"]

def remove_special_characters(path):
    """Remove special characters from a path.
    
    Args:
        path (str): Path to clean.
    
    Returns:
        str: Cleaned path.
    """
    for specialCharacter in SPECIALCHARACTERSLIST:
        path = path.replace(specialCharacter, "_")

    return path

class TemplateManager():
    """Class to manage projects templates paths.
    """
    def __init__(self):
        pass

    @staticmethod
    def get_template_path_for_entity(template, working=False, publish=False, parent_entity="asset", target_entity="Project"):
        """Get the template path for entity.
        
        Args:
            template (str): Project template.
            working (bool, optional): Use working path.
            publish (bool, optional): Use publish path.
            parent_entity (str, optional): Type of entity to target, can be "asset" or "shot".
            target_entity (str, optional): Type of entity to get.
        
        Returns:
            str: Template path.
        
        Raises:
            CoreError: Can be related to not correct value for `parent_entity` or missing `working`/`publish` argument.
        """
        if(parent_entity not in ["asset", "shot"]):
            raise CoreError("Parent entity can only be either \"asset\" or \"shot\".")

        # Path type.
        if(working and not publish):
            template_type = template["working"]
        elif(not working and publish):
            template_type = template["output"]
        else:
            raise CoreError("Get template can only find path for working path OR publish path (not both).")

        # Entity to look for.
        entity_to_find = "{"+target_entity+"}"

        original_template = os.path.join(template_type["mountpoint"], template_type["root"], template_type["folder_path"][parent_entity])

        new_template = ""
        for current_template_part in original_template.split("/"):
            new_template += current_template_part
            new_template += "/"
            if(current_template_part == entity_to_find):
                return new_template

        raise CoreError("Failed to find a match for {}".format(target_entity))

    @staticmethod
    def get_folderpath(exportType="output", project=None, category=None, entity=None, task_type=None, version_number=-1):
        """Get the folderpath for entity.

        Args:
            exportType (str, optional): Export type, "output" ou "working". Defaults to "output".
            project (class:`Project`): Project to apply template
            category (class:`Category`): Category of the entity. Defaults to None.
            entity (class:`Entity`): Entity. Defaults to None.
            task_type (class:`Task`): Task. Defaults to None.
            version_number (int): Version of the entity.

        Returns:
            str: Folder path.
        """
        from ..pmObj.asset import Asset

        if(version_number == -1):
            raise CoreError("Version need to be specified to get the folderpath.")

        if(exportType not in ["output", "working"]):
            raise CoreError("Export type can only be \"output\" or \"working\".")

        template = project.paths_template
        project_name = project.name
        category_name = category.name
        entity_name = entity.name
        task_name = task_type.name.lower()

        # This is need because our production filetree on IZES isn't correctly setup.
        if(type(entity) == type(Asset())):
            category_name = category_name.lower()
            entity_type = "asset"
        else:
            entity_type = "shot"

        path = os.path.join(template[exportType]["mountpoint"],
                            template[exportType]["root"],
                            template[exportType]["folder_path"][entity_type])
        
        path = path.format(Project=project_name,
                            AssetType=category_name,
                            Sequence=category_name,
                            Asset=entity_name,
                            Shot=entity_name,
                            TaskType=task_name,
                            Version=version_number)

        del(Asset)

        return remove_special_characters(path)

    @staticmethod
    def get_folderpath_from_template(template="", project=None, category=None, entity=None, task_type=None, version_number=-1):
        """Get the path from a template.
        
        Args:
            template (str): Template to use
            project (class:`Project`): Project to apply template
            category (class:`Category`): Category of the entity. Defaults to None.
            entity (class:`Entity`): Entity. Defaults to None.
            task_type (class:`Task`): Task. Defaults to None.
            version_number (int): Version of the entity.
        
        Returns:
            str: Path on the disk.
        """
        project_name = project.name
        category_name = category.name
        entity_name = entity.name

        if(task_type == None):
            task_name = ""
        else:
            task_name = task_type.name.lower()

        path = template.format(Project=project_name,
                            AssetType=category_name,
                            Sequence=category_name,
                            Asset=entity_name,
                            Shot=entity_name,
                            TaskType=task_name,
                            Version=version_number)

        return remove_special_characters(path)

    @staticmethod
    def get_filename(exportType="output", project=None, category=None, entity=None, task_type=None, version_number=-1):
        """Get the filename for the entity.

        Args:
            exportType (str, optional): Export type, "output" ou "working". Defaults to "output".
            project (class:`Project`): Project to apply template
            category (class:`Category`): Category of the entity. Defaults to None.
            entity (class:`Entity`): Entity. Defaults to None.
            task_type (class:`Task`): Task. Defaults to None.
            versionNumber (int): Version of the entity.

        Returns:
            str: File name.
        """
        from ..pmObj.asset import Asset

        if(version_number == -1):
            raise CoreError("Version need to be specified to get the folderpath.")

        if(exportType not in ["output", "working"]):
            raise CoreError("Export type can only be \"output\" or \"working\".")

        template = project.paths_template
        project_name = project.name
        category_name = category.name
        entity_name = entity.name
        task_name = task_type.name.lower()

        # This is need because our production filetree on IZES isn't correctly setup.
        if(type(entity) == type(Asset())):
            category_name = category_name.lower()
            entity_type = "asset"
        else:
            entity_type = "shot"

        filename = template[exportType]["file_name"][entity_type]
        
        filename = filename.format(Project=project_name,
                                    AssetType=category_name,
                                    Sequence=category_name,
                                    Asset=entity_name,
                                    Shot=entity_name,
                                    TaskType=task_name,
                                    Version=version_number)

        filename = remove_special_characters(filename)

        del(Asset)

        return filename


    @staticmethod
    def build_folder_tree(project):
        """Build the foldertree for the project.

        Args:
            project (class:`Project`): Project to build on disk.

        Returns:
            bool: Status.
        """
        for category in project.categories:
            for entity in category.entities:
                for task in entity.tasks:
                    FileManager().make_folder(TemplateManager().get_folderpath(exportType="working", project=project, category=category, entity=entity, task_type=task, version_number=0))
                    FileManager().make_folder(TemplateManager().get_folderpath(exportType="output", project=project, category=category, entity=entity, task_type=task, version_number=0))
        
        return True

class FileManager():
    """Class to manipulate files on disk.
    """
    def __init__(self):
        pass

    @property
    def temp_directory(self):
        """Get the path to the temporary folder.
        
        Returns:
            str: Path.
        """
        path = os.path.join(tempfile.gettempdir(), "hestia")

        # If temporary folder not exist, we make it.
        if(not os.path.isdir(path)):
            self.make_folder(path)

        return path
    

    @staticmethod
    def make_folder(path):
        """Build a folder.

        Args:
            path (str): Folder path.

        Returns:
            bool: Creation status.
        """
        if(not os.path.isdir(path)):
            try:
                os.makedirs(path)
            except OSError as error:
                print("Directory %s can't be created (%s)" % (path, error))
                return False
            else:
                return True
        else:
            return False

    @staticmethod
    def copy_file(filePath, targetPath, **kwargs):
        """Copy a file from a directory to another.

        Args:
            filePath (str): Input path.
            targetPath (str): Output path.

        Returns:
            bool: Copy status.
        """
        oldFilename = os.path.split(filePath)[1]
        if(not os.path.isfile(targetPath + os.sep + oldFilename)):
            shutil.copy(filePath, targetPath)

            if(isinstance(kwargs["new_name"], str)):
                extension = kwargs["new_extension"] if "new_extension" in kwargs else os.path.splitext(oldFilename)[1][1:]
                dst = targetPath + os.sep + kwargs["new_name"] + "." + extension

                if(os.path.isfile(dst) != True):
                    src = targetPath + os.sep + oldFilename
                    os.rename(src, dst)

            return True
        return False