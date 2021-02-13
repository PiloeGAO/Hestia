"""
    :package:   Hestia
    :file:      folderTreeView.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the folder tree of the window.  
"""
from Qt import QtCore, QtWidgets, QtGui

class FolderTreeView(QtWidgets.QWidget):
    CATEGORY, NONE = range(2) # NONE is set to be able to add new header data to treeview in future.

    def __init__(self, parent=None):
        """Folder tree Class.

        Args:
            parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
        """
        super(FolderTreeView, self).__init__(parent=parent)

        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the main layout component.
        self.mainLayout = QtWidgets.QVBoxLayout()

        # Creating the base of the TreeView.
        self.treeView = QtWidgets.QTreeView()
        self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)

        # Creating the cutom gui item model.
        model = QtGui.QStandardItemModel(0, 1, self)
        model.setHeaderData(self.CATEGORY, QtCore.Qt.Horizontal, "Category")

        # Assign model to tree view.
        self.treeView.setModel(model)

        # Add demy items to tree view.
        self.addItem(model, "Category 01")
        self.addItem(model, "Category 02")
        self.addItem(model, "Category 03")

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