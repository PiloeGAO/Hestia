"""
    :package:   Hestia
    :file:      preferences.py
    :brief:     Preference class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.4
"""
try:
    import configparser
except:
    import ConfigParser as configparser

import os

class Preferences():
    def __init__(self, manager=None):
        self.__manager = manager

        self.__path = os.path.expanduser("~") + os.sep + ".hestia.config"

        self.__config = configparser.RawConfigParser()
    
    @property
    def config(self):
        """Get config from preferences.

        Returns:
            class:'ConfigParser' : config.
        """
        return self.__config
    
    @config.setter
    def config(self, config):
        """Set config for preferences.

        Args:
            config (class: 'ConfigParser'): config.
        """
        self.__config = config
    
    def getValue(self, section, key, valueType="str"):
        """Get the value from config file.

        Args:
            section (str): Section of the save file.
            key (str): Data key.

        Returns:
            str: Value
        """
        try:
            value = self.__config.get(section, key)
        except configparser.Error as err:
            print("Failed to get value: %s" % err)
            return None
        else:
            return value
    
    def setValue(self, section, key, value):
        """Set a value in config.

        Args:
            section (str): Section of the save file.
            key (str): Data key.

        Returns:
            bool: Status.
        """
        try:
            self.__config.set(section, key, value)
        except configparser.Error as err:
            print("Failed to get value: %s" % err)
            return False
        else:
            return True
    
    def generatePreferences(self):
        """Building base preference system.
        """
        self.__config.add_section("MANAGER")
        
        self.__config.set("MANAGER", "version", self.__manager.version)
        self.__config.set("MANAGER", "windowPos", "-1x-1")
        self.__config.set("MANAGER", "windowSize", "-1x-1")
        self.__config.set("MANAGER", "debugMode", 0)
        self.__config.set("MANAGER", "service", "kitsu")
        self.__config.set("MANAGER", "onlineHost", "")
        self.__config.set("MANAGER", "onlineUsername", "")
        self.__config.set("MANAGER", "rememberLogin", 1)
        self.__config.set("MANAGER", "loadPreviews", 1)
    
    def loadPreferences(self):
        """Load local preferences.
        """
        self.__config.read(self.__path)
        if(self.__config.sections() == []):
            print("Failed to load preferences.")
            return False
        else:
            return True
    
    def savePreferences(self):
        """save local preferences.
        """
        try:
            with open(self.__path, "w") as configfile:
                self.__config.write(configfile)
        except OSError as err:
            self.__manager.logging.error("Saving preferences OS error: {0}".format(err))
            return False
        else:
            return True