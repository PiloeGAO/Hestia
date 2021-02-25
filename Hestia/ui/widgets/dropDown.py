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

        self.__name = name
        self.__description = description
        self.__datas = datas
        self.__currentValue = defaultValue if defaultValue > 0 and defaultValue < len(self.__datas) else 0

        self.initUI()
    
    @property
    def currentValue(self):
        """Return index of the selected value in dropdown.

        Returns:
            int: Index.
        """
        return self.__currentValue
    
    @property
    def datas(self):
        """Returnt the datas stored in the dropdown.

        Returns:
            list: Datas.
        """
        return self.__datas
    
    @datas.setter
    def datas(self, newDatas):
        """Set new datas to dropdown.

        Args:
            newDatas (list): New Datas.
        """
        self.__datas = newDatas

        self.dropDown.clear()
        self.dropDown.addItems(self.__datas)
        self.update()
    
    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Vertical.
        self.mainLayout = QtWidgets.QHBoxLayout()

        # Create title.
        self.title = QtWidgets.QLabel(self.__name + " : ")

        # Add description as tooltip.
        self.title.setToolTip(self.__description)

        # Add title to main layout.
        self.mainLayout.addWidget(self.title)

        # Create ComboBox.
        self.dropDown = QtWidgets.QComboBox()

        # Add datas to drop down.
        self.dropDown.addItems(self.__datas)

        # Set default index to dropdown.
        self.dropDown.setCurrentIndex(self.__currentValue)

        # Connect dropdown with update method.
        self.dropDown.currentIndexChanged.connect(self.changeCurrentValue)

        # Add ComboBox to main layout.
        self.mainLayout.addWidget(self.dropDown)

        # Add the main layout to the window.
        self.setLayout(self.mainLayout)
    
    def changeCurrentValue(self):
        """Set current value from drop down.
        """
        self.__currentValue = self.dropDown.currentIndex()