"""
    :package:   Hestia
    :file:      mainWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
    :brief:     Class to create the main window based on QtWidgets.  
"""
import sys

global pysideVers
try:
    from PySide2.QtCore     import *
    from PySide2.QtGui      import *
    from PySide2.QtWidgets  import *
    pysideVers = 2
except:
    from PySide.QtCore      import *
    from PySide.QtGui       import *
    pysideVers = 1

from .core.manager          import start_manager, current_manager

from .loginWindow           import LoginWindow
from .publishWindow         import PublishWindow
from .preferencesWindow     import PreferencesWindow

from .ui.header             import Header
from .ui.folderTreeView     import FolderTreeView
from .ui.contentView        import ContentView
from .ui.footer             import Footer

class MainWindow(QWidget):
    """Main Window class.

    Args:
        manager (class: "Manager"): Manager of Hestia.
        parent (class: "QtWidgets", optional): PyQt parent. Defaults to None.
    """
    def __init__(self, manager=None, integration="standalone", parent=None):
        super(MainWindow, self).__init__(parent=parent)
        # Defining the Manager.
        self.__manager = manager
        if(self.__manager == None):
            try:
                self.__manager = start_manager(integration=integration)
            except RuntimeError:
                self.__manager = current_manager()

        # TODO: Test this with the correct versions.
        # Display warning message when PySide1 or Python 2 is used.
        if(pysideVers == 1 or sys.version_info[0] == 2):
            self.__manager.logging.warning("PySide 1 and Python 2.XX are deprecated, please upgrade.")

        # Set window preferences.
        self.__windowWidth, self.__windowHeight = [int(coord) for coord in self.__manager.preferences.getValue("MANAGER", "windowSize").split("x")]
        self.__posX, self.__posY                = [int(coord) for coord in self.__manager.preferences.getValue("MANAGER", "windowPos").split("x")]

        desktopGeometry = QDesktopWidget().screenGeometry(-1)
        titleBarHeigth = 10
        if(self.__windowWidth < 0 or self.__windowWidth > desktopGeometry.width()):
            self.__windowWidth = desktopGeometry.width() / 4
        if(self.__windowHeight < 0 or self.__windowHeight > desktopGeometry.height()):
            self.__windowHeight = desktopGeometry.height() / 4
        if(self.__posX < 0 or self.__posX > (desktopGeometry.width() - self.__windowWidth)):
            self.__posX = desktopGeometry.width() / 2 - self.__windowWidth / 2
        if(self.__posY < 0 or self.__posY > (desktopGeometry.height() - self.__windowHeight - titleBarHeigth)):
            self.__posY = desktopGeometry.height() / 2 - self.__windowHeight / 2 - titleBarHeigth

        # Initialize UI.
        self.initUI()

        # Initialize the publish window.
        self.publishWindow = None

        # Initialize the preference window.
        self.preferencesWindow = None

        # Show online login modal if not set to local.
        self.loginWindow = None
        if(self.__manager.mode != "local" and not self.__manager.link.connected):
            self.loginWindow = LoginWindow(manager=self.__manager, mainWindow=self)
            self.loginWindow.show()
    
    def resizeEvent(self, event):
        """Get the size of the window on window resize.

        Args:
            event (class: "QtEvent"): Event.
        """
        QWidget.resizeEvent(self, event)
        self.__manager.preferences.setValue("MANAGER", "windowSize", "%ix%i"%(self.width(), self.height()))
    
    def moveEvent(self, event):
        """Get the position of the window on window move.

        Args:
            event (class: "QtEvent"): Event.
        """
        QWidget.moveEvent(self, event)
        self.__manager.preferences.setValue("MANAGER", "windowPos", "%ix%i"%(self.x(), self.y()))
    
    def closeEvent(self, event):
        """Get the close event on window close.

        Args:
            event (class: 'QtEvent'): Event.
        """
        if(True):
            # Closing other window if Main Window is closed.
            if(self.loginWindow != None): self.loginWindow.hide()
            if(self.preferencesWindow != None): self.preferencesWindow.hide()
            if(self.publishWindow != None): self.publishWindow.hide()
            """
            if(self.__manager.integration.name != "standalone"):
                # This is needed for embedded Python versions
                # that won't support *atexit* lib.
                self.__manager.preferences.savePreferences()
                self.__manager.cleanTemporaryFolder()
            """
            event.accept()
        else:
            event.ignore()
    
    def initUI(self):
        """Generate the window.
        """
        # Set the window title.
        self.setWindowTitle("Hestia Browser")
        
        # Set the window size.
        self.setGeometry(self.__posX, self.__posY,
                        self.__windowWidth, self.__windowHeight)

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
        self.contentView = ContentView(manager=self.__manager, mainWindow=self)
        self.mainLayout.addWidget(self.contentView, 1, 1, 1, 3)

        # Add footer to window.
        self.footer = Footer(manager=self.__manager)
        self.mainLayout.addWidget(self.footer, 2, 0, 1, 4)
        self.footer.updateLog(text="Welcome to Hestia!")

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def openPreferencesWindow(self):
        """Display the preferences window.
        """
        self.preferencesWindow = PreferencesWindow(manager=self.__manager)
        self.preferencesWindow.show()
    
    def openPublishWindow(self, entity):
        """Display the publish window.

        Args:
            entity (class:`Entity`): Entity datas to publish.
        """
        if(self.publishWindow != None):
            self.publishWindow.close()
            self.publishWindow = None
        self.publishWindow = PublishWindow(mainWindow=self, entity=entity)
        self.publishWindow.show()

    def updateLog(self, text=""):
        """Update log in the footer.

        Args:
            text (str, optional): Text to display. Defaults to "".
        """
        self.footer.updateLog(text=text)
        self.footer.refresh()

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
