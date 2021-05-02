"""
    :package:   Hestia
    :file:      iconButton.py
    :brief:     Button with icon.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
"""
import os

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

class IconButton(QWidget):
    """Icon Button class.

    Args:
        name (str, optional): Text of the button. Defaults to "".
        description (str, optional): Tooltip. Defaults to "".
        iconPath (str, optional): Path to icon. Defaults to "".
        iconScale (int, optional): Icon scale in pixels. Defaults to 64.
        status (int, optional): Status of the button, 0 is disable and 1 is enable. Defaults to 1.
        functionToInvoke ([type], optional): Function to activate on button click. Defaults to None.
        parent ([type], optional): Parent widget. Defaults to None.
    """
    def __init__(self, name="", description="", iconPath="", iconScale=64, status=1, functionToInvoke=None, parent=None):
        super(IconButton, self).__init__(parent=parent)

        self._name = name
        self._description = description
        self._iconPath = iconPath
        self._iconScale = iconScale
        self._status = status
        self._functionToInvoke = functionToInvoke

        self.initUI()
    
    @property
    def iconScale(self):
        """Return icon scale in pixel.
        """
        return self._iconScale
    
    @iconScale.setter
    def iconScale(self, scale):
        """Set new icon scale.

        Args:
            scale (int): Icon scale in pixels.
        """
        self._iconScale = scale
        self.button.setIconSize(QSize(self._iconScale, self._iconScale))
        self.update()
    
    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Vertical.
        self.mainLayout = QVBoxLayout()
        
        # Set spacing and margin for the current layout.
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Create a button.
        self.button = QPushButton()

        # Add Icon to button.
        if(os.path.isfile(self._iconPath)):
            # Add Icon to button.
            self.button.setIcon(QIcon(self._iconPath))
            self.button.setIconSize(QSize(self._iconScale, self._iconScale))
        else:
            # Add text to button.
            self.button.setText(self._name)
        
        # Add description as tooltip.
        self.button.setToolTip(self._description)

        # Link button with it's function.
        self.button.clicked.connect(self._functionToInvoke)

        # Set button status.
        self.button.setEnabled(self._status)

        # Add button to layout.
        self.mainLayout.addWidget(self.button)

        # Add the main layout to the window.
        self.setLayout(self.mainLayout)
    
    def changeButtonStatus(self, status):
        """Change button status.

        Args:
            status (int): Button status, 0 is disable and 1 is enable.
        """
        # Change status variable.
        self._status = status

        # Update button setEnabled.
        self.button.setEnabled(status)

        # Update widget.
        self.update()