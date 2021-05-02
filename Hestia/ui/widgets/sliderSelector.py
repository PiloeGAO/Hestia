"""
    :package:   Hestia
    :file:      sliderSelector.py
    :brief:     Slider with labels under it.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.2
"""

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

class SliderSelector(QWidget):
    """Slider Selector class.

    Args:
        name (str, optional): Text of the button. Defaults to "".
        description (str, optional): Tooltip. Defaults to "".
        datas (list, optional): Data array (Strings or integers only). Defaults to [].
        defaultValue (int, optional): Default value ID. Defaults to 0.
        parent (QtWidgets, optional): Parent widget. Defaults to None.
    """
    def __init__(self, name="", description="", datas=[], defaultValue=0, parent=None):
        super(SliderSelector, self).__init__(parent=parent)

        self._name = name
        self._description = description
        self._datas = datas
        self._currentValue = defaultValue if defaultValue >= 0 and defaultValue < len(self._datas) else 0

        self.initUI()
    
    @property
    def currentValue(self):
        """Return current value of the slider.

        Returns:
            int: Slider index value.
        """
        return self._currentValue
    
    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Vertical.
        self.mainLayout = QGridLayout()

        # Create title.
        self.title = QLabel(self._name + " : ")

        # Add description as tooltip.
        self.title.setToolTip(self._description)

        # Add title to main layout.
        self.mainLayout.addWidget(self.title, 0, 0, 1, 1)

        # Create slider.
        self.slider = QSlider(Qt.Horizontal)

        # Set minimum and maximum value.
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self._datas)-1)

        # Set default value.
        self.slider.setValue(self._currentValue)

        # Set tick intervals.
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)

        # Set slider ticks below.
        self.slider.setTickPosition(QSlider.TicksBelow)

        # Connect slider with update method.
        self.slider.valueChanged.connect(self.changeCurrentValue)

        # Add slider to main layout.
        self.mainLayout.addWidget(self.slider, 0, 1, 0, len(self._datas)-1)

        # Create empty label for alignment.
        self.sliderLabelEmpty = QLabel(" ")

        # Add empty label to mainLayout.
        self.mainLayout.addWidget(self.sliderLabelEmpty, 1, 0, 1, 1)

        # Create labels under slider.
        for i, currentData in enumerate(self._datas):
            # Convert data to string before displaying it.
            if type(currentData) != str:
                currentData = str(currentData)
            
            self.sliderLabel = QLabel(currentData)

            self.mainLayout.addWidget(self.sliderLabel, 1, 1 + i, 1, 1)

        # Add the main layout to the window.
        self.setLayout(self.mainLayout)
    
    def changeCurrentValue(self):
        """Set current value from drop down.
        """
        self._currentValue = self.slider.value()