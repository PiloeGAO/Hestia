"""
    :package:   Hestia
    :file:      mainWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the main window based on QtWidgets.  
"""
from Qt import QtWidgets

from .ui.header         import Header
from .ui.folderTreeView import FolderTreeView
from .ui.contentView    import ContentView
from .ui.footer         import Footer

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """Main Window Class.

        Args:
            parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
        """
        super(MainWindow, self).__init__(parent=parent)

        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the window title.
        self.setWindowTitle("Hestia")
        
        # Set the window size.
        self.resize(640, 480)

        # Set the window style.
        self.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

        # Set the main layout component.
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setSpacing(10)

        # Add header to window.
        self.header = Header()
        self.mainLayout.addWidget(self.header, 0, 0, 1, 4)

        # Add tree view.
        self.folderTreeView = FolderTreeView()
        self.mainLayout.addWidget(self.folderTreeView, 1, 0, 1, 1)

        # Add content view.
        self.contentView = ContentView()
        self.mainLayout.addWidget(self.contentView, 1, 1, 1, 3)

        # Add footer to window.
        self.footer = Footer()
        self.mainLayout.addWidget(self.footer, 2, 0, 1, 4)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)