"""
    :package:   Hestia
    :file:      launchHestiaBrowser.py
    :author:    ldepoix
    :version:   0.0.4
    :brief:     Class to start UI from Guerilla Render.
"""
from guerilla   import Modifier, Document, pwarning
from guerilla   import command, Node

class LaunchHestiaBrowser(command):

    @staticmethod
    def isenabled(luaObj, window):
        return True

    @staticmethod
    def action(luaObj, window, x, y, suffix):
        import os, sys
        from PySide                 import QtGui
        from Hestia.mainWindow      import MainWindow
        from Hestia.core.manager    import *

        manager = None
        try:
            manager = start_manager(integration="Guerilla")
        except RuntimeError:
            manager = current_manager()
        
        app = QtGui.QApplication.instance()
        if(app is None):
            app = QtGui.QApplication(sys.argv)
        app.setStyle('Plastique')

        globals()['qtHestiaBrowserWindow'] = MainWindow(manager=manager)
        globals()['qtHestiaBrowserWindow'].show()

cmd = LaunchHestiaBrowser('Hestia Browser')
cmd.install('Edit', 'Hestia')