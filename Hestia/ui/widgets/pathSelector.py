"""
    :package:   Hestia
    :file:      pathSelector.py
    :brief:     Path field with search button.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from Qt             import QtWidgets

class PathSelector(QtWidgets.QWidget):
    """Icon Button class.

    Args:
        name (str, optional): Text of the button. Defaults to "".
        description (str, optional): Tooltip. Defaults to "".
        path (str, optional): Default path. Defaults to "".
        isDir (bool, optional): Is path to directory or file. Defaults to True.
        parent ([type], optional): Parent widget. Defaults to None.
    """
    def __init__(self, name="", description="", path="", isDir=True, parent=None):
        super(PathSelector, self).__init__(parent=parent)

        self._name = name
        self._description = description
        self._path = path
        self._pathIsDir = isDir

        self.initUI()
    
    @property
    def path(self):
        """Get path stored in the widget.

        Returns:
            str: Path.
        """
        return self._path
    
    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Vertical.
        self.mainLayout = QtWidgets.QHBoxLayout()

        # Create title.
        self.title = QtWidgets.QLabel(self._name + " : ")

        # Add description as tooltip.
        self.title.setToolTip(self._description)

        # Add title to main layout.
        self.mainLayout.addWidget(self.title)

        # Create line edit to display path.
        self.pathDisplay = QtWidgets.QLineEdit(self._path)

        # Connect QLineEdit to editPath.
        self.pathDisplay.textEdited.connect(self.editPath)

        # Add display path to main layout.
        self.mainLayout.addWidget(self.pathDisplay)

        # Create browse button.
        self.browseButton = QtWidgets.QPushButton("Browse")

        # Connect button to browse method.
        self.browseButton.clicked.connect(self.browseFunction)

        # Add browse button to main layout.
        self.mainLayout.addWidget(self.browseButton)

        # Add the main layout to the window.
        self.setLayout(self.mainLayout)
    
    def editPath(self):
        """Update path in widget variable if QLineEdit is edited.
        """
        self._path = self.pathDisplay.text()

    def browseFunction(self):
        """Open popup to select the targeted directory.
        """
        if(self._pathIsDir):
            path = QtWidgets.QFileDialog.getExistingDirectory(self, "Open " + self._name,
                                       self._path,
                                       QtWidgets.QFileDialog.ShowDirsOnly
                                       | QtWidgets.QFileDialog.DontResolveSymlinks)
        else:
            path = QtWidgets.QFileDialog.getOpenFileName(self,
                                                "Open " + self._name,
                                                self._path,
                                                "*")[0]
        # Set path in widget variable.
        self._path = path

        # Set text in QLineEdit.
        self.pathDisplay.setText(path)