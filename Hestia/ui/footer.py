"""
    :package:   Hestia
    :file:      footer.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
    :brief:     Class to create the footer of the window.  
"""
try:
    from PySide2.QtCore     import *
    from PySide2.QtGui      import *
    from PySide2.QtWidgets  import *
except:
    from PySide.QtCore      import *
    from PySide.QtGui       import *

class Footer(QWidget):
    """Footer Class.

    Args:
        manager (class: "Manager"): The hestia manager.
        parent (class: "QtWidgets.QWidget", optional): The parent widget. Defaults to None.
    """
    def __init__(self, manager, parent=None):
        super(Footer, self).__init__(parent=parent)

        self.__manager = manager

        self.version = self.__manager.version

        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """

        # Set the main layout component.
        self.mainLayout = QHBoxLayout()

        # Add current logged in user.
        self.logWidget = QLabel("")
        self.mainLayout.addWidget(self.logWidget)

        # Add spacer to footer.
        self.mainLayout.addStretch()

        # Add current logged in user.
        self.currentVersion = QLabel("V %s" % self.version)
        self.mainLayout.addWidget(self.currentVersion)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def updateLog(self, text=""):
        """Update the log widget of the footer.

        Args:
            text (str, optional): Text to display. Defaults to "".
        """
        self.logWidget.setText(text)

    def refresh(self):
        """Force refresh of the widget.
        """
        self.update()