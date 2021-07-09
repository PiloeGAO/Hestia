"""
    :package:   Hestia
    :file:      videoButton.py
    :brief:     Button with video as icon.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
"""
import os
import platform

try:
    from PySide2.QtCore     import *
    from PySide2.QtGui      import *
    from PySide2.QtWidgets  import *
except:
    from PySide.QtCore      import *
    from PySide.QtGui       import *

import vlc


from ...core.logger import get_logging
logger = get_logging(__name__)

class VideoButton(QWidget):
    """Video Button class.
    (Initial work from: https://git.videolan.org/?p=vlc/bindings/python.git;a=blob;f=examples/pyqt5vlc.py;h=cb3d29488c9efe43a80ae8d17e083137b368487d;hb=HEAD )

    Args:
        name (str, optional): Text of the button. Defaults to "".
        description (str, optional): Tooltip. Defaults to "".
        iconPath (str, optional): Path to icon. Defaults to "".
        iconScale (int, optional): Icon scale in pixels. Defaults to 64.
        status (int, optional): Status of the button, 0 is disable and 1 is enable. Defaults to 1.
        functionToInvoke (function, optional): Function to activate on button click. Defaults to None.
        parent (class: `QWidget`, optional): Parent widget. Defaults to None.
    """
    def __init__(self, name="", description="", iconPath="", iconScale=64, status=1, functionToInvoke=None, parent=None):
        super(VideoButton, self).__init__(parent=parent)

        self._name = name
        self._description = description
        self._iconPath = iconPath
        self._iconScale = iconScale
        self._status = status
        self._functionToInvoke = functionToInvoke

        # Create a basic vlc instance
        self.instance = vlc.Instance()

        self.mediaplayer = self.instance.media_player_new()

        self.is_paused = False

        self.initUI()

        if(not os.path.isfile(self._iconPath)):
            logger.warning("videoButton widget: file {} not found.".format(self._iconPath))
        else:
            # Add media to mediaplayer.
            self.media = self.instance.media_new(self._iconPath)

            # Put the media in the media player
            self.mediaplayer.set_media(self.media)

            # Parse media metadatas.
            self.media.parse()

            # The media player has to be 'connected' to the QFrame (otherwise the
            # video would be displayed in it's own window). This is platform
            # specific, so we must give the ID of the QFrame (or similar object) to
            # vlc. Different platforms have different functions for this
            if platform.system() == "Linux": # for Linux using the X Server
                self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
            elif platform.system() == "Windows": # for Windows
                self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
            elif platform.system() == "Darwin": # for MacOS
                self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
            
            # Init display.
            self.mediaplayer.set_position(0.0)

            # Set video size.
            self.videoframe.setFixedSize(self.mediaplayer.video_get_width()/4,
                                        self.mediaplayer.video_get_height()/4)

            # Ajust video scale to frame.
            self.mediaplayer.video_set_scale(0)

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
        #self.button.setIconSize(QSize(self._iconScale, self._iconScale))
        self.update()

    def mousePressEvent(self, event):
        if(event.type() == QEvent.MouseButtonPress):
            if(event.button() == Qt.LeftButton):
                self._functionToInvoke()

    def enterEvent(self, event):
        self.play()
    
    def leaveEvent(self, event):
        self.stop()

    def initUI(self):
        """Main UI creation function.
        """
        # Setting the main layout as Vertical.
        self.mainLayout = QVBoxLayout()
        
        # Set spacing and margin for the current layout.
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.videoframe = QFrame()

        self.palette = self.videoframe.palette()
        self.palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)
                                        
        self.mainLayout.addWidget(self.videoframe)

        # Add the main layout to the window.
        self.setLayout(self.mainLayout)

    def play_pause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.is_paused = True
        else:
            if self.mediaplayer.play() == -1:
                return

            self.mediaplayer.play()
            self.is_paused = False
    
    def play(self):
        """Toggle play status
        """
        if(not self.mediaplayer.is_playing()):
            if self.mediaplayer.play() == -1:
                return
            
            self.mediaplayer.play()
            self.is_paused = False

    def pause(self):
        """Toggle pause status
        """
        if(self.mediaplayer.is_playing()):
            self.mediaplayer.pause()
            self.is_paused = True

    def stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
    
    def changeButtonStatus(self, status):
        """Change button status.

        Args:
            status (int): Button status, 0 is disable and 1 is enable.
        """
        # Change status variable.
        self._status = status

        # Update button setEnabled.
        #self.button.setEnabled(status)

        # Update widget.
        self.update()