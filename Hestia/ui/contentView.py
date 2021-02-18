"""
    :package:   Hestia
    :file:      contentView.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the content view of the window.  
"""
from Qt import QtWidgets

from .widgets.entityWidget import EntityWidget
class ContentView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        """Content view Class.

        Args:
            parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
        """
        super(ContentView, self).__init__(parent=parent)

        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the main layout component.
        self.mainLayout = QtWidgets.QGridLayout()

        for i in range(4):
            for j in range(4):
                entity = EntityWidget(name="Demo",
                                      description="Demo description",
                                      iconPath="./ui/icons/alarm.svg",
                                      iconSize=64,
                                      status=1,
                                      versionList=["001", "002"])
                self.mainLayout.addWidget(entity, i, j)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)