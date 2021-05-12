"""
    :package:   Hestia
    :file:      publishWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
    :brief:     Class to create the publish window based on QtWidgets.  
"""

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

class PublishWindow(QWidget):
    """Publish Window class.

    Args:
        manager (class: "Manager"): Manager of Hestia.
        parent (class: "QtWidgets", optional): PyQt parent. Defaults to None.
    """
    def __init__(self, manager, parent=None):
        super(PublishWindow, self).__init__(parent=parent)
        self.__manager      = manager

        self.initUI()

    def initUI(self):
        """Generate the window.
        """

        # Set the window title.
        self.setWindowTitle("Hestia - Publish")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        
        #self.resize(self.__windowWidth, self.__windowHeight)

        # Set the window style.
        self.setStyle(QStyleFactory.create("Fusion"))

        # Set the main layout component.
        self.mainLayout = QVBoxLayout()

        demoButton = QPushButton("DEMO")
        self.mainLayout.addWidget(demoButton)

        # Set main layout to the window.
        self.setLayout(self.mainLayout)
    
    def displayWindow(self):
        """Initialize/reset and show the window.
        """
        self.show()