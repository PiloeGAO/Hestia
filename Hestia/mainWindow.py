"""
    :package:   Hestia
    :file:      mainWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the main window based on QtWidgets.  
"""
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

from .core.manager    import Manager

from .loginWindow       import LoginWindow

from .ui.header         import Header
from .ui.folderTreeView import FolderTreeView
from .ui.contentView    import ContentView
from .ui.footer         import Footer

class MainWindow(QWidget):
    """Main Window class.

    Args:
        manager (class: "Manager", optional): Manager of Hestia. Defaults to Manager().
        mode (str, optional): Manager mode. Defaults to "local".
        winW (int, optional): Window width. Defaults to 640.
        winH (int, optional): Window height. Defaults to 480.
        parent (class: "QtWidgets", optional): PyQt parent. Defaults to None.
    """
    def __init__(self, manager=Manager(integration="standalone"), mode="local", winW = 640, winH = 480, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        # Defining the Manager.
        self.__manager = manager

        # Set window preferences.
        self.__windowWidth = winW
        self.__windowHeight = winH

        self.initUI()

        if(mode != "local" and not self.__manager.link.connected):
            login = LoginWindow(manager=self.__manager, mainWindow=self, service=mode)
            login.show()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the window title.
        self.setWindowTitle("Hestia Browser")
        
        # Set the window size.
        self.resize(self.__windowWidth, self.__windowHeight)

        # Set the window style.
        self.setStyle(QStyleFactory.create("Fusion"))

        # Set the main layout component.
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(10)

        # Add header to window.
        self.header = Header(manager=self.__manager, mainWindow=self)
        self.mainLayout.addWidget(self.header, 0, 0, 1, 4)

        # Add tree view.
        self.folderTreeView = FolderTreeView(manager=self.__manager, mainWindow=self)
        self.folderTreeView.setMaximumWidth(self.__windowWidth/3)
        self.mainLayout.addWidget(self.folderTreeView, 1, 0, 1, 1)

        # Add content view.
        self.contentView = ContentView(manager=self.__manager)
        self.mainLayout.addWidget(self.contentView, 1, 1, 1, 3)

        # Add footer to window.
        self.footer = Footer(manager=self.__manager)
        self.mainLayout.addWidget(self.footer, 2, 0, 1, 4)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def refresh(self):
        """Force refresh of the window.
        """
        self.header.refresh()
        self.folderTreeView.refresh()
        self.contentView.refresh()
        self.footer.refresh()
    
    def refreshProject(self):
        """Refresh the window on project change.
        """
        self.folderTreeView.refresh()
        self.contentView.refresh()
    
    def refreshCategory(self):
        """Refresh the window on category change.
        """
        self.contentView.refresh()
