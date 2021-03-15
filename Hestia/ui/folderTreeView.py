"""
    :package:   Hestia
    :file:      folderTreeView.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the folder tree of the window.  
"""
from Qt import QtCore, QtWidgets, QtGui

from .widgets.dropDown          import DropDown
from .widgets.categoryWidget    import CategoryWidget

class FolderTreeView(QtWidgets.QWidget):
    """Folder tree Class.

    Args:
        manager(class: "Manager"): The Hestia manager.
        mainWindow(class: "MainWindow"): The Hestia main window.
        parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
    """
    def __init__(self, manager, mainWindow, parent=None):
        super(FolderTreeView, self).__init__(parent=parent)
        self.__manager      = manager
        self.__mainWindow   = mainWindow

        self.__project      = self.__manager.projects[self.__manager.currentProject]

        self.__availableTypes = ["Assets", "Shots"]
        self.__categories = [category for category in self.__project.categories if category.type == self.__availableTypes[0]]
        
        self.initUI()
    
    def resizeEvent(self, event):
        """Resize the widget when window is resized by user.

        Args:
            event (class: "QtEvent"): Event.
        """
        QtWidgets.QWidget.resizeEvent(self, event)
        self.refresh()
    
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
                                functionToInvoke=self.changeCurrentCategoryType)
        self.mainLayout.addWidget(self.type)

        # Creating the base of the TreeView (ScrollArea).
        self.scrollArea = QtWidgets.QScrollArea()

        self.categoriesLayout = QtWidgets.QVBoxLayout()
        #self.categoriesLayout.setContentsMargins(0, 0, 0, 0)

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
                categoryButton = CategoryWidget(manager=self.__manager, mainWindow=self.__mainWindow, category=category, parentWidget=self)
                self.categoriesLayout.addWidget(categoryButton)
            
            try:
                # Reset the size of the layout properly.
                self.categoriesWidget.setFixedWidth(self.scrollArea.size().width() - 20)
                self.categoriesWidget.setFixedHeight(self.scrollArea.size().height())
            except AttributeError:
                pass
        
        else:
            noCategoryText = QtWidgets.QLabel("No categories available.")
            self.categoriesLayout.addWidget(noCategoryText)
        
        self.update()
    
    def cleanTree(self):
        """Clean the category tree.
        """
        # Removing the old widgets.
        for i in reversed(range(self.categoriesLayout.count())):
            self.categoriesLayout.itemAt(i).widget().setParent(None)
        
        self.update()
    
    def changeCurrentCategoryType(self):
        """Updating the current selected category when type change.
        """
        category = [category for category in self.__project.categories if category.type == self.__availableTypes[self.type.currentValue]][0]
        
        if category != None:
            self.__project.currentCategory = self.__project.categories.index(category)
        
        self.__mainWindow.refreshCategory()
        self.refresh()
    
    def refresh(self):
        """Force refresh of the widget.
        """
        self.cleanTree()
        
        self.__project    = self.__manager.projects[self.__manager.currentProject]
        self.__categories = [category for category in self.__project.categories if category.type == self.__availableTypes[self.type.currentValue]]

        self.buildTree()

        self.update()