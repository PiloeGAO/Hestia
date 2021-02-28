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
        xSize (int, optional): Number of widgets on X axis. Defaults to 4.
        parent (class: "QtWidget", optional): Parent widget. Defaults to None.
    """
    def __init__(self, manager, xSize=4, parent=None):
        super(ContentView, self).__init__(parent=parent)
        self.__manager  = manager
        self.__project  = self.__manager.projects[self.__manager.currentProject]

        self.__category = Category(name="Empty", type="Assets")
        if(len(self.__project.categories) > 0):
            self.__category = self.__project.categories[self.__project.currentCategory]

        self.__entities = self.__category.entities

        self.xSize = xSize

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
        entitiesCount = len(self.__entities)
        
        if(entitiesCount > 0):
            ySize = entitiesCount % self.xSize + 1

            for y in range(ySize):
                for x in range(self.xSize):
                    count = x + y * ySize
                    if(count < entitiesCount):
                        # Getting entity datas.
                        name = self.__entities[count].name
                        description = self.__entities[count].description

                        icon = self.__entities[count].icon
                        if(icon == ""):
                            icon = "./ui/icons/alarm.svg"
                        
                        versions = self.__entities[count].versions
                        
                        # Create the widget.
                        entity = EntityWidget(name=name,
                                            description=description,
                                            iconPath=icon,
                                            iconSize=64,
                                            status=1,
                                            versionList=versions)
                        
                        self.grid.addWidget(entity, y, x)
            
                    # Reset the size of the grid properly.
                    self.grid.setColumnMinimumWidth(x, (self.scrollArea.size().width() - 20)/4)
                    self.grid.setRowMinimumHeight(y, (self.scrollArea.size().height() - 20)/4)
            
            # Reset the size of the widget.
            self.widget.setFixedWidth(self.scrollArea.size().width() - 20)
            self.widget.setFixedHeight(self.scrollArea.size().height() - 20)
            
        else:
            entity = QtWidgets.QLabel("No entities found.")
            self.grid.addWidget(entity, 0, 0)

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
        self.cleanEntitiesGrid()

        # Updating variables.
        self.__project  = self.__manager.projects[self.__manager.currentProject]

        self.__category = Category(name="Empty", type="Assets")
        if(len(self.__project.categories) > 0):
            self.__category = self.__project.categories[self.__project.currentCategory]

        self.__entities = self.__category.entities

        # ---------------------------------------------

        self.buildEntitiesGrid()

        self.update()