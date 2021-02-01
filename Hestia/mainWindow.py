"""
    :package:   Hestia
    :file:      mainWindow.py
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
    :brief:     Class to create the main window based on QtWidgets.  
"""
from Qt import QtWidgets

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
        self.mainLayout = QtWidgets.QVBoxLayout()

        # Set main layout to the window.
        self.setLayout(self.mainLayout)