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
        from Hestia.core.manager    import Manager

        hestiaManager = Manager(integration="Guerilla")
        
        app = QtGui.QApplication.instance()
        if(app is None):
            app = QtGui.QApplication(sys.argv)
        app.setStyle('Plastique')

        globals()['qtHestiaBrowserWindow'] = MainWindow(manager=hestiaManager)
        globals()['qtHestiaBrowserWindow'].show()

cmd = LaunchHestiaBrowser('Hestia Browser')
cmd.install('Edit', 'Hestia')