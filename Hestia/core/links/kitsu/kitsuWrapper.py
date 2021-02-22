"""
    :package:   Hestia
    :file:      kitsuWrapper.py
    :brief:     Kitsu wrapper class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

import gazu

class KitsuWrapper():
    def __init__(self, api="", username="", password=""):
        self.__api      = api
        self.__username = username
        self.__password = password
        self.__active   = False

        try:
            gazu.client.set_host(self.__api)
        except gazu.exception.HostException:
            self.__active = False
        else:
            self.__active = True

    def login(self):
        """Login to Gazu.

        Returns:
            bool: State of the login.
        """
        if (self.__active == False):
            return False

        try:
            gazu.log_in(self.__username, self.__password)
        except gazu.exception.AuthFailedException:
            return False
        else:
            return True
