"""
    :package:   Hestia
    :file:      categoryWidget.py
    :brief:     Category widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
"""
try:
    from PySide2.QtCore     import *
    from PySide2.QtGui      import *
    from PySide2.QtWidgets  import *
except:
    from PySide.QtCore      import *
    from PySide.QtGui       import *

from .iconButton            import IconButton

class CategoryWidget(QWidget):
    """Entity widget display class.

        Args:
            manager(class: "Manager"): The Hestia manager.
            category(class: "Category"): The category to display.
            parentWidget(class: "FolderTreeView"): Parent of the widget.
            parent (class: "QtWidget", optional): Parent. Defaults to None.
    """
    def __init__(self, manager, mainWindow, category, parentWidget, parent=None):
        super(CategoryWidget, self).__init__(parent=parent)

        self.__manager      = manager
        self.__mainWindow   = mainWindow
        self.__parent       = parentWidget

        self.__project      = self.__manager.projects[self.__manager.currentProject]

        self.__category     = category
        self.__categoryID   = self.__project.categories.index(self.__category)

        self.__current_categoryID = self.__project.current_category
        self.__current_category = self.__project.categories[self.__current_categoryID]

        self.active = 1
        if(self.__current_category == self.__category):
            self.active = 0

        self.initUI()
    
    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Horizontal.
        self.mainLayout = QVBoxLayout()

        self.categoryButton = IconButton(name=self.__category.name,
                                         description=self.__category.description,
                                         status=self.active,
                                         functionToInvoke=self.set_current_category)
        
        self.mainLayout.addWidget(self.categoryButton)

        self.setLayout(self.mainLayout)
    
    def set_current_category(self):
        """Change the current category of the project.
        """
        self.__manager.projects[self.__manager.currentProject].current_category = self.__categoryID
        self.__parent.refresh()
        self.__mainWindow.refreshCategory()