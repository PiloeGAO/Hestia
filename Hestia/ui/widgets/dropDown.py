"""
    :package:   Hestia
    :file:      dropDown.py
    :brief:     Drop down field with text.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

class DropDown(QWidget):
    """Drop Down class.

    Args:
        name (str, optional): Text of the button. Defaults to "".
        description (str, optional): Tooltip. Defaults to "".
        datas (list, optional): Data array (Strings or integers only). Defaults to [].
        defaultValue (int, optional): Default value ID. Defaults to 0.
        functionToInvoke (function, optional): Function to invoke on currentIndexChanged. Defaults to None.
        parent (QtWidgets, optional): Parent widget. Defaults to None.
    """
    def __init__(self, name="", description="", datas=[], defaultValue=0, functionToInvoke = None, parent=None):
        super(DropDown, self).__init__(parent=parent)

        self.__name = name
        self.__description = description
        self.__datas = datas
        self.__currentValue = 0

        if(defaultValue > 0 and defaultValue < len(self.__datas)):
            self.__currentValue = defaultValue

        self.__functionToInvoke = functionToInvoke

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
        self.mainLayout = QHBoxLayout()

        # Create title.
        self.title = QLabel(self.__name + " : ")

        # Add description as tooltip.
        self.title.setToolTip(self.__description)

        # Add title to main layout.
        self.mainLayout.addWidget(self.title)

        # Create ComboBox.
        self.dropDown = QComboBox()

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
        if(self.dropDown.currentIndex() >= 0):
            self.__currentValue = self.dropDown.currentIndex()

            if(self.__functionToInvoke != None):
                self.__functionToInvoke()