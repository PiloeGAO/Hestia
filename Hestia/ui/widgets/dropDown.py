"""
    :package:   Hestia
    :file:      dropDown.py
    :brief:     Drop down field with text.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

from Qt             import QtWidgets

class DropDown(QtWidgets.QWidget):
    """Drop Down class.

    Args:
        name (str, optional): Text of the button. Defaults to "".
        description (str, optional): Tooltip. Defaults to "".
        datas (list, optional): Data array (Strings or integers only). Defaults to [].
        defaultValue (int, optional): Default value ID. Defaults to 0.
        parent (QtWidgets, optional): Parent widget. Defaults to None.
    """
    def __init__(self, name="", description="", datas=[], defaultValue=0, parent=None):
        super(DropDown, self).__init__(parent=parent)

        self._name = name
        self._description = description
        self._datas = datas
        self._currentValue = defaultValue if defaultValue > 0 and defaultValue < len(self._datas) else 0

        self.initUI()
    
    @property
    def currentValue(self):
        """Return index of the selected value in dropdown.

        Returns:
            int: Index.
        """
        return self._currentValue
    
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

        # Create ComboBox.
        self.dropDown = QtWidgets.QComboBox()

        # Add datas to drop down.
        self.dropDown.addItems(self._datas)

        # Set default index to dropdown.
        self.dropDown.setCurrentIndex(self._currentValue)

        # Connect dropdown with update method.
        self.dropDown.currentIndexChanged.connect(self.changeCurrentValue)

        # Add ComboBox to main layout.
        self.mainLayout.addWidget(self.dropDown)

        # Add the main layout to the window.
        self.setLayout(self.mainLayout)
    
    def changeCurrentValue(self):
        """Set current value from drop down.
        """
        self._currentValue = self.dropDown.currentIndex()