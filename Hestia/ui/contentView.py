"""
    :package:   Hestia
    :file:      contentView.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the content view of the window.  
"""
from Qt import QtWidgets, QtCore

from .widgets.entityWidget import EntityWidget
class ContentView(QtWidgets.QWidget):

    def __init__(self, xNumber=4, yNumber=3, parent=None):
        """Content view Class.

        Args:
            parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
        """
        super(ContentView, self).__init__(parent=parent)

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

        for i in range(self.yNumber):
            for j in range(self.xNumber):
                entity = EntityWidget(name="Demo",
                                      description="Demo description",
                                      iconPath="./ui/icons/alarm.svg",
                                      iconSize=64,
                                      status=1,
                                      versionList=["001", "002"])
                self.grid.addWidget(entity, i, j)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.grid)

        self.scrollArea.setWidget(self.widget)

        self.mainLayout.addWidget(self.scrollArea)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)

    def refresh(self):
        """Force refresh of the widget.
        """
        self.update()