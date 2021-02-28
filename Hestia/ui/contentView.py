"""
    :package:   Hestia
    :file:      contentView.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the content view of the window.  
"""
from Qt import QtWidgets, QtCore

from ..core.category        import Category

from .widgets.entityWidget  import EntityWidget
class ContentView(QtWidgets.QWidget):
    """Content View class.

    Args:
        manager (class: "Manager"): The Hestia manager.
        xNumber (int, optional): Number of widgets on X axis. Defaults to 4.
        yNumber (int, optional): Number of widgets on Y axis. Defaults to 3.
        parent (class: "QtWidget", optional): Parent widget. Defaults to None.
    """
    def __init__(self, manager, xNumber=4, yNumber=3, parent=None):
        super(ContentView, self).__init__(parent=parent)
        self.__manager  = manager
        self.__project  = self.__manager.projects[self.__manager.currentProject]

        self.__category = Category(name="Empty", type="Assets")
        if(len(self.__project.categories) > 0):
            self.__category = self.__project.categories[self.__project.currentCategory]

        self.xNumber = xNumber
        self.yNumber = yNumber

        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the main layout component.
        self.mainLayout = QtWidgets.QHBoxLayout()

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(False)
        self.scrollArea.setHorizontalScrollBarPolicy(False)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)

        self.buildEntitiesGrid()

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.grid)

        self.scrollArea.setWidget(self.widget)

        self.mainLayout.addWidget(self.scrollArea)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)

    def buildEntitiesGrid(self):
        """Build the entities grid.
        """
        for i in range(self.yNumber):
            for j in range(self.xNumber):
                entity = EntityWidget(name="Demo",
                                      description="Demo description",
                                      iconPath="./ui/icons/alarm.svg",
                                      iconSize=64,
                                      status=1,
                                      versionList=["001", "002"])
                self.grid.addWidget(entity, i, j)

        self.update
    
    def cleanEntitiesGrid(self):
        """Clean the entities grid.
        """
        # Removing the old widgets.
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)
        
        self.update

    def refresh(self):
        """Force refresh of the widget.
        """
        self.update()