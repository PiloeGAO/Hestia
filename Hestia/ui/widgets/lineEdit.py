"""
    :package:   Hestia
    :file:      lineEdit.py
    :brief:     Drop down field with text.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.3
"""
try:
    from PySide2.QtCore     import *
    from PySide2.QtGui      import *
    from PySide2.QtWidgets  import *
except:
    from PySide.QtCore      import *
    from PySide.QtGui       import *

class LineEdit(QWidget):
    """Line Edit class.

    Args:
        name (str, optional): Text of the button. Defaults to "".
        description (str, optional): Tooltip. Defaults to "".
        defaultValue (str, optional): Default value ID. Defaults to "".
        isPassword (bool, optional): Hide characters for passwords/credentials. Defaults to False.
        parent (QtWidgets, optional): Parent widget. Defaults to None.
    """
    def __init__(self, name="", description="", defaultValue="", isPassword=False, parent=None):
        super(LineEdit, self).__init__(parent=parent)

        self.__name = name
        self.__description = description
        self.__currentValue = defaultValue

        self.__isPassword = isPassword

        self.initUI()
    
    @property
    def currentValue(self):
        """Return value of the selected value in lineEdit.

        Returns:
            str: value.
        """
        return self.__currentValue
    
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

        # Create the line edit.
        self.lineEdit = QLineEdit()
        self.lineEdit.setText(self.__currentValue)

        if(self.__isPassword):
            self.lineEdit.setEchoMode(QLineEdit.Password)

        # Connect line edit with update method.
        self.lineEdit.textChanged.connect(self.changeCurrentValue)
        self.lineEdit.returnPressed.connect(self.changeCurrentValue)

        # Add line edit to main layout.
        self.mainLayout.addWidget(self.lineEdit)

        # Add the main layout to the window.
        self.setLayout(self.mainLayout)
    
    def changeCurrentValue(self):
        """Set current value from drop down.
        """
        self.__currentValue = self.lineEdit.text()