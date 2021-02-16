"""
    :package:   Hestia
    :file:      footer.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the footer of the window.  
"""
from Qt import QtWidgets

class Footer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """Footer Class.

        Args:
            parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
        """
        super(Footer, self).__init__(parent=parent)

        self.user = "DEMO"
        self.version = "0.0.1"

        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the main layout component.
        self.mainLayout = QtWidgets.QHBoxLayout()

        # Add current logged in user.
        self.currentUser = QtWidgets.QLabel("Current user: %s" % self.user)
        self.mainLayout.addWidget(self.currentUser)

        # Add spacer to footer.
        self.mainLayout.addStretch()

        # Add current logged in user.
        self.currentVersion = QtWidgets.QLabel("V %s" % self.version)
        self.mainLayout.addWidget(self.currentVersion)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)