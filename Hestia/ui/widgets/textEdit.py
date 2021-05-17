"""
    :package:   Hestia
    :file:      textEdit.py
    :brief:     Text Edit field with title.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
"""
try:
    from PySide2.QtCore     import *
    from PySide2.QtGui      import *
    from PySide2.QtWidgets  import *
except:
    from PySide.QtCore      import *
    from PySide.QtGui       import *

class TextEdit(QWidget):
    """Text Edit class.

    Args:
        name (str, optional): Text of the button. Defaults to "".
        description (str, optional): Tooltip. Defaults to "".
        defaultValue (str, optional): Default value ID. Defaults to "".
        parent (QtWidgets, optional): Parent widget. Defaults to None.
    """
    def __init__(self, name="", description="", defaultValue="", parent=None):
        super(TextEdit, self).__init__(parent=parent)

        self.__name = name
        self.__description = description
        self.__currentValue = defaultValue

        self.initUI()
    
    @property
    def currentValue(self):
        """Return value of the selected value in textEdit.

        Returns:
            str: value.
        """
        return self.__currentValue
    
    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Vertical.
        self.mainLayout = QVBoxLayout()

        # Create title.
        self.title = QLabel(self.__name + " : ")

        # Add description as tooltip.
        self.title.setToolTip(self.__description)

        # Add title to main layout.
        self.mainLayout.addWidget(self.title)

        # Create the text edit.
        self.textEdit = QTextEdit()
        self.textEdit.setText(self.__currentValue)

        # Connect text edit with update method.
        self.textEdit.textChanged.connect(self.changeCurrentValue)

        # Add text edit to main layout.
        self.mainLayout.addWidget(self.textEdit)

        # Add the main layout to the window.
        self.setLayout(self.mainLayout)
    
    def changeCurrentValue(self):
        """Set current value from drop down.
        """
        self.__currentValue = self.textEdit.toPlainText()