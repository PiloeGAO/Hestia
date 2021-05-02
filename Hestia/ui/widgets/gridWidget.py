"""
    :package:   Hestia
    :file:      gridWidget.py
    :brief:     Custom grid system for PyQt.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

from .entityWidget import EntityWidget

class GridWidget(QWidget):
    """Grid Widget class.

    Args:
        parent (QtWidgets, optional): Parent widget. Defaults to None.
    """
    def __init__(self, manager, parentGeometry, xSize=2, itemList=[], emptyLabel="Grid empty", parent=None):
        super(GridWidget, self).__init__(parent=parent)
        self.__manager = manager
        self.__parentGeometry = parentGeometry

        self.__itemList = itemList
        self.__itemListSize = len(itemList)

        self.__xSize = int(xSize)
        self.__ySize = int(self.__itemListSize / self.__xSize + self.__itemListSize % self.__xSize)

        self.__emptyLabel = emptyLabel

        self.initUI()
    
    def initUI(self):
        """Main UI creation function.
        """
        # Set the main layout component.
        self.mainLayout = QVBoxLayout()

        if(self.__itemListSize > 0):
            self.mainLayout.setSpacing(0)
            self.mainLayout.setContentsMargins(0, 0, 0, 0)

            # Build the loop for QHBoxLayout creation.
            for y in range(self.__ySize):
                # Creating the horizontal layout for X.
                horizontalLayout = QHBoxLayout()
                horizontalLayout.setSpacing(0)
                horizontalLayout.setSizeConstraint(QLayout.SetMaximumSize)
                horizontalLayout.setContentsMargins(0, 0, 0, 0)

                for x in range(self.__xSize):
                    itemCount = x + y * self.__xSize

                    if(itemCount < self.__itemListSize):
                        # Create the widget.
                        item = self.__itemList[itemCount]
                                            
                    else:
                        # Add empty string if no item available to keep grid.
                        item = QLabel("")
                    
                    item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    item.setMinimumWidth(self.__parentGeometry.width()/self.__xSize - 10)
                    horizontalLayout.addWidget(item)
                
                self.mainLayout.addLayout(horizontalLayout)
        
        else:
            self.textDisplay = QLabel(self.__emptyLabel)
            self.mainLayout.addWidget(self.textDisplay)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)