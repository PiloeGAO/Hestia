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
    def __init__(self, manager, parent=None):
        """Folder tree Class.

        Args:
            parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
        """
        super(FolderTreeView, self).__init__(parent=parent)
        self.__manager = manager

        self.__availableTypes = ["Assets", "Shots"]
        self.__categories = [str(category.name) for category in self.__manager.projects[self.__manager.currentProject].categories if category.type == self.__availableTypes["Assets"]]
        
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
                                defaultValue=0,
                                functionToInvoke=self.refresh)
        self.mainLayout.addWidget(self.type)

        # Creating the base of the TreeView (ScrollArea).
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(False)
        self.scrollArea.setHorizontalScrollBarPolicy(False)

        self.categoriesLayout = QtWidgets.QVBoxLayout()
        self.categoriesLayout.setContentsMargins(0, 0, 0, 0)

        self.buildTree()

        self.categoriesWidget = QtWidgets.QWidget()
        self.categoriesWidget.setLayout(self.categoriesLayout)

        self.scrollArea.setWidget(self.categoriesWidget)
        self.mainLayout.addWidget(self.scrollArea)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def buildTree(self):
        """Build the category tree.
        """

        if(len(self.__categories) > 0):
            for category in self.__categories:
                categoryButton = QtWidgets.QPushButton(category)
                self.categoriesLayout.addWidget(categoryButton)
        
        else:
            noCategoryText = QtWidgets.QLabel("No categories available.")
            self.categoriesLayout.addWidget(noCategoryText)
        
        
        self.update()
    
    def cleanTree(self):
        """Clean the category tree.
        """
        # Removing the old widgets.
        for item in reversed(range(self.categoriesLayout.count())):
            childWidget = self.categoriesLayout.takeAt(item)
            del childWidget
        
        self.update()
    
    def refresh(self):
        """Force refresh of the widget.
        """
        # Not working: I can't find a way to properly clear the self.categoriesLayout.
        self.cleanTree()

        del self.__categories[:]
        self.__categories = [str(category.name) for category in self.__manager.projects[self.__manager.currentProject].categories if category.type == self.__availableTypes[self.type.currentValue]]
        self.buildTree()

        self.update()