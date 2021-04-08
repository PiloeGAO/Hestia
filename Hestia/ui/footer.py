"""
    :package:   Hestia
    :file:      footer.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the footer of the window.  
"""
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

class Footer(QWidget):
    def __init__(self, manager, parent=None):
        """Footer Class.

        Args:
            manager (class: "Manager"): The hestia manager.
            parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
        """
        super(Footer, self).__init__(parent=parent)

        self.__manager = manager

        self.user = self.__manager.link.username
        self.version = self.__manager.version

        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the main layout component.
        self.mainLayout = QHBoxLayout()

        # Add current logged in user.
        self.currentUser = QLabel("Current user: %s" % self.user)
        self.mainLayout.addWidget(self.currentUser)

        # Add spacer to footer.
        self.mainLayout.addStretch()

        # Add current logged in user.
        self.currentVersion = QLabel("V %s" % self.version)
        self.mainLayout.addWidget(self.currentVersion)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def refresh(self):
        """Force refresh of the widget.
        """
        self.user = self.__manager.link.username
        self.currentUser.setText("Current user: %s" % self.user)
        self.update()