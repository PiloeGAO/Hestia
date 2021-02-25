"""
    :package:   Hestia
    :file:      folderTreeView.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the folder tree of the window.  
"""
from Qt import QtCore, QtWidgets, QtGui

from .widgets.dropDown import DropDown

class FolderTreeView(QtWidgets.QWidget):
    CATEGORY, NONE = range(2) # NONE is set to be able to add new header data to treeview in future.

    def __init__(self, manager, parent=None):
        """Folder tree Class.

        Args:
            parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
        """
        super(FolderTreeView, self).__init__(parent=parent)
        self.__manager = manager

        self.__availableTypes = ["Assets", "Shots"]
        self.__categories = ["Category 01", "Category 02", "Category 03"]

        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the main layout component.
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Add type dropdown.
        self.type = DropDown(name="Type",
                                description="The type of category",
                                datas=self.__availableTypes,
                                defaultValue=0)
        self.mainLayout.addWidget(self.type)

        # Creating the base of the TreeView.
        self.treeView = QtWidgets.QTreeView()
        self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)

        # Creating the cutom gui item model.
        self.categoryModel = QtGui.QStandardItemModel(0, 1, self)
        self.categoryModel.setHeaderData(self.CATEGORY, QtCore.Qt.Horizontal, "Category")

        # Assign model to tree view.
        self.treeView.setModel(self.categoryModel)

        # Add demy items to tree view.
        self.addItems(self.categoryModel, self.__categories)

        # Adding the treeview to mainLayout.
        self.mainLayout.addWidget(self.treeView)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def addItem(self, model, name):
        """Add item to tree view.

        Args:
            model (class: "QtGui.QStandardItemModel"): Model.
            name (str): Category/Folder name.
        """
        model.insertRow(0)
        model.setData(model.index(0, self.CATEGORY), name)
    
    def addItems(self, model, names=[]):
        """Add items to tree view.

        Args:
            model (class: "QtGui.QStandardItemModel"): Model.
            name (str): Category/Folder name list. Defaults to [].
        """
        for name in names:
            self.addItem(model, name)
    
    def refresh(self):
        """Force refresh of the widget.
        """
        # Not working > Find a better way to display the treeview.
        self.categoryModel.clear()
    
        self.__categories = [str(category.name) for category in self.__manager.projects[self.__manager.currentProject].categories if category.type == self.__availableTypes[self.type.currentValue]]

        self.addItems(self.categoryModel, self.__categories)

        self.update()