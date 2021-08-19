"""
    :package:   Hestia
    :file:      stage.py
    :brief:     USD Stage class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import os

try:
    from pxr import Usd, UsdGeom
except ImportError:
    raise CoreError("Please add USD in your PYTHONPATH and PATH,\nthe procedure can be found here: https://graphics.pixar.com/usd/docs/USD-Tutorials.html")

from ..exceptions import CoreError

class USDStage(object):
    def __init__(self, path=""):
        """USD Stage class.
        
        Args:
            path (str, optional): Path to USD file.
        """
        self._path = path

    @property
    def path(self):
        """Get the path stored in the class.
        
        Returns:
            str: Path to file.
        """
        return self._path

    @property
    def content(self):
        """Get the content of a USD Stage.
        
        Returns:
            str: String representation of the stage.
        """
        return self.root_layer.ExportToString()

    @property
    def get_stage(self):
        """Get the stage from path.
        
        Returns:
            class:`stage`: Stage.
        """
        return Usd.Stage.Open(self._path)

    @property
    def root_layer(self):
        """Get the root layer of the stage.
        
        Returns:
            class:`rootLayer`: Root layer of the stage.
        """
        return self.get_stage.GetRootLayer()

    def create_stage(self):
        """Create the stage on disk.
        """
        if(not os.path.isfile(self._path)):
            stage = Usd.Stage.CreateNew(self._path)
            return stage.Save()
        return False

    def set_time_range(self, start_frame, end_frame):
        """Set time range for the stage.
        
        Args:
            start_frame (int): Start frame.
            end_frame (int): End frame.
        """
        stage = self.get_stage
        stage.SetStartTimeCode(start_frame)
        stage.SetEndTimeCode(end_frame)
        stage.Save()

    def set_up_axis(self, axis="z"):
        """Set Up axis for the stage.
        
        Args:
            axis (str): Axis to choose, must be "x", "y" or "z"
        
        Raises:
            CoreError: Invalid axis
        """
        stage = self.get_stage

        if(not axis in ["x", "y", "z"]):
            raise CoreError("Invalid Up Axis for stage.")

        token = UsdGeom.Tokens.x
        if(axis == "y"):
            token = UsdGeom.Tokens.y
        elif(axis == "z"):
            token = UsdGeom.Tokens.z

        UsdGeom.SetStageUpAxis(stage, token)
        stage.Save()

    def set_stage_metadata(self, key, value):
        """Set a metadata to stage.
        
        Args:
            key (str): Key name.
            value (str): Value to set.
        """
        stage = Usd.Stage.Open(self._path)
        stage.SetMetadata(key, value)
        stage.Save()

    def get_metadata(self, prim, key):
        """Get Metadata for a primitive. 
        
        Args:
            prim (class:`usdPrim`): Target primitive.
            key (str): Key.
        
        Returns:
            str: Value.
        """
        return prim.GetMetadata(key)

    def set_metadata(self, prim, key, value):
        """Set Metadata for a primitive.
        
        Args:
            prim (class:`usdPrim`): Target primitive.
            key (str): Key name.
            value (str): Value to set.
        
        Returns:
            bool: Status
        """
        return prim.SetMetadata(key, value)

    def get_prim_at_path(self, path):
        """Get primitive from a path.
        
        Args:
            path (str): Path to primitive.
        
        Returns:
            class:`usdPrim: Primitive.
        """
        return self.get_stage.GetPrimAtPath(path)

    def set_default_prim(self, prim):
        """Set the default primitive for the stage.
        
        Args:
            prim (class:`usdPrim`): Primitive to set as default.
        
        Returns:
            bool: Status.
        """
        stage = self.get_stage
        status = stage.SetDefaultPrim(prim)
        stage.Save()
        return status

    def get_properties_for_prim(self, prim):
        """Get properties name for primitive.
        
        Args:
            prim (class:`usdPrim`): Primitive to check.
        
        Returns:
            list: Properties names.
        """
        return prim.GetPropertyNames()

    def get_attribute(self, prim, attribute_name):
        """Get attribute value for primitive.
        
        Args:
            prim (class:`usdPrim`): Primitive.
            attribute_name (str): Attribute name.
        
        Returns:
            Value of the attribute.
        """
        return prim.GetAttribute(attribute_name_name).Get()

    def set_attribute(self, prim, attribute_name, value):
        """Set attribute value for primitive.
        
        Args:
            prim (class:`usdPrim`): Primitive.
            attribute_name (str): Attribute name.
            value (?): Value to set.
        
        Returns:
            bool: Set status.
        """
        stage = self.get_stage
        status = prim.GetAttribute(attribute_name).Set(value)
        stage.Save()
        return status