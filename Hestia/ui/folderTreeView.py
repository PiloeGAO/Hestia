"""
    :package:   Hestia
    :file:      folderTreeView.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.3
    :brief:     Class to create the folder tree of the window.  
"""
try:
    from PySide2.QtCore         import *
    from PySide2.QtGui          import *
    from PySide2.QtWidgets      import *
except:
    from PySide.QtCore          import *
    from PySide.QtGui           import *

from .widgets.dropDown          import DropDown
from .widgets.categoryWidget    import CategoryWidget
from .widgets.gridWidget        import GridWidget

class FolderTreeView(QWidget):
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
        QWidget.resizeEvent(self, event)
        self.refresh()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the main layout component.
        self.mainLayout = QVBoxLayout()
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
        self.scrollArea = QScrollArea()

        self.grid = GridWidget(manager=self.__manager,
                                parentGeometry=self.scrollArea.geometry(),
                                xSize=1,
                                itemList=self.buildCategoryList(),
                                emptyLabel="No categories availables.")

        self.scrollArea.setWidget(self.grid)

        self.mainLayout.addWidget(self.scrollArea)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def changeCurrentCategoryType(self):
        """Updating the current selected category when type change.

        Returns:
            bool: Status.
        """
        category = [category for category in self.__project.categories if category.type == self.__availableTypes[self.type.currentValue]]
        if(len(category) > 0):
            category = category[0]
        else:
            return False
        
        if category != None:
            self.__project.currentCategory = self.__project.categories.index(category)
        
        self.__mainWindow.refreshCategory()
        self.refresh()
        return True
    
    def refresh(self):
        """Force refresh of the widget.
        """
        # Updating variables.
        self.__project    = self.__manager.projects[self.__manager.currentProject]
        self.__categories = [category for category in self.__project.categories if category.type == self.__availableTypes[self.type.currentValue]]

        # Updating the grid with a new grid.
        self.grid = GridWidget(manager=self.__manager,
                                parentGeometry=self.scrollArea.geometry(),
                                xSize=1,
                                itemList=self.buildCategoryList(),
                                emptyLabel="No categories availables.")
        
        self.scrollArea.setWidget(self.grid)

        self.update()
    
    def buildCategoryList(self):
        """Build the category array.

        Returns:
            list: (class:"CategoryWidget"): Array of CategoryWidget.
        """
        categoriesList = []
        for category in self.__categories:
            categoryButton = CategoryWidget(manager=self.__manager,
                                            mainWindow=self.__mainWindow,
                                            category=category,
                                            parentWidget=self)

            categoriesList.append(categoryButton)
        
        return categoriesList