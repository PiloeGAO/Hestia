"""
    :package:   Hestia
    :file:      user.py
    :brief:     User class.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""
from .entity import Entity

class User(Entity):
    """User class.

    Args:
        username (str, optional): Username.
        email (str, optional): Mail of the user.
        phone (str, optional): Phone of the user.
        role (str, optional): Role of the user.
    """
    def __init__(self, username="", email="", phone="", role="", *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._username = username
        self._email    = email
        self._phone    = phone
        self._role     = role
    
    @property
    def username(self):
        """Get the user name.

        Returns:
            str: User name
        """
        return self._username
    
    @property
    def email(self):
        """Get the email of the user.

        Returns:
            str: User email
        """
        return self._email
    
    @property
    def phone(self):
        """Get the phone of the user.

        Returns:
            str: Phone number
        """
        return self._phone
    
    @property
    def role(self):
        """Get the role of the user.

        Returns:
            str: Role
        """
        return self._role