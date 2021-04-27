"""
    :package:   Hestia
    :file:      contentView.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the content view of the window.  
"""
import os

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

from ..core.category        import Category

from .widgets.gridWidget    import GridWidget
from .widgets.entityWidget  import EntityWidget

class ContentView(QWidget):
    """Content View class.

    Args:
        manager (class: "Manager"): The Hestia manager.
        xSize (int, optional): Number of widgets on X axis. Defaults to 4.
        parent (class: "QtWidget", optional): Parent widget. Defaults to None.
    """
    def __init__(self, manager, xSize=2, parent=None):
        super(ContentView, self).__init__(parent=parent)
        self.__manager  = manager
        self.__project  = self.__manager.projects[self.__manager.currentProject]
        
        self.__rootPath = os.path.dirname(os.path.abspath(__file__))

        self.__category = Category(name="Empty", type="Assets")
        if(len(self.__project.categories) > 0):
            self.__category = self.__project.categories[self.__project.currentCategory]

        self.__entities = self.__category.entities

        self.xSize = xSize

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
        self.mainLayout = QHBoxLayout()

        self.scrollArea = QScrollArea()

        self.grid = GridWidget(manager=self.__manager, parentGeometry=self.scrollArea.geometry(), xSize=self.xSize, itemList=self.__entities)
        
        self.scrollArea.setWidget(self.grid)

        self.mainLayout.addWidget(self.scrollArea)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)

    def refresh(self):
        """Force refresh of the widget.
        """
        # Updating variables.
        self.__project  = self.__manager.projects[self.__manager.currentProject]

        self.__category = Category(name="Empty", type="Assets")
        if(len(self.__project.categories) > 0):
            self.__category = self.__project.categories[self.__project.currentCategory]

        self.__entities = self.__category.entities

        # Updating the grid with a new grid.
        self.grid = GridWidget(manager=self.__manager, parentGeometry=self.scrollArea.geometry(), xSize=self.xSize, itemList=self.__entities)
        self.scrollArea.setWidget(self.grid)

        self.update()