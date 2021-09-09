"""
    :package:   Hestia
    :file:      preferences.py
    :brief:     Preference class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
import os

import configparser

from .logger    import get_logging, shutdown_logger
logger = get_logging()

preferences_template = {
    "MANAGER" : [
        {
            "name" : "version",
            "type" : "string",
            "default" : "0.0.0",
            "description" : "Manager version"
        },
        {
            "name" : "windowPos",
            "type" : "string",
            "default" : "-1x-1",
            "description" : "Window Position"
        },
        {
            "name" : "windowSize",
            "type" : "string",
            "default" : "-1x-1",
            "description" : "Window Size"
        },
        {
            "name" : "service",
            "type" : "string",
            "default" : "kitsu",
            "description" : "Service used by Hestia"
        },
        {
            "name" : "windowSize",
            "type" : "string",
            "default" : "-1x-1",
            "description" : "Window Size"
        },
        {
            "name" : "rememberLogin",
            "type" : "int",
            "default" : "1",
            "description" : "Allow the software to save your credentials"
        },
        {
            "name" : "loadPreviews",
            "type" : "int",
            "default" : "1",
            "description" : "Download preview images"
        }
    ],
    "MAYA" : [],
    "KITSU" : [
        {
            "name" : "host",
            "type" : "string",
            "default" : "",
            "description" : "URL for the host"
        },
        {
            "name" : "username",
            "type" : "string",
            "default" : "user@example.com",
            "description" : "User mail"
        }
    ]
}

class Preferences():
    def __init__(self, manager=None):
        self._manager = manager

        self._path = os.path.join(os.path.expanduser("~"), ".hestia.config")

        self._config = configparser.RawConfigParser()
    
    @property
    def config(self):
        """Get config from preferences.

        Returns:
            class:'ConfigParser' : config.
        """
        return self._config
    
    @config.setter
    def config(self, config):
        """Set config for preferences.

        Args:
            config (class: 'ConfigParser'): config.
        """
        self._config = config
    
    def getValue(self, section, key, valueType="str"):
        """Get the value from config file.

        Args:
            section (str): Section of the save file.
            key (str): Data key.

        Returns:
            str: Value
        """
        try:
            value = self._config.get(section, key)
        except configparser.Error as err:
            logger.error("Failed to get value: %s" % err)

            # Add missing datas to preferences.
            if(not section in self._config.sections()):
                self._config.add_section(section)

            if(len([entry for entry in self._config[section] if entry == key]) == 0):
                items = [item for item in preferences_template[section]]

                if(len(items) == 0):
                    return None

                item = items[0]
                self._config.set(section, item["name"], item["default"])

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
            self._config.set(section, key, value)
        except configparser.Error as err:
            logger.error("Failed to set value: %s" % err)
            return False
        else:
            return True
    
    def generatePreferences(self):
        """Building base preference system.
        """
        for section in preferences_template:
            self._config.add_section(section)

            for item in preferences_template[section]:
                self._config.set(section, item["name"], item["default"])
    
    def loadPreferences(self):
        """Load local preferences.
        """
        self._config.read(self._path)
        if(self._config.sections() == []):
            logger.error("Failed to load preferences.")
            return False
        else:
            return True
    
    def savePreferences(self):
        """save local preferences.
        """
        try:
            with open(self._path, "w") as configfile:
                self._config.write(configfile)
        except OSError as err:
            logger.error("Saving preferences OS error: {0}".format(err))
            return False
        else:
            return True