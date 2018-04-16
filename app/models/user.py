import re

class User:
    users = []
    
    @classmethod
    def register_user(cls, username, email, password):
        user = cls()
        user.username = username
        user.email = email
        user.password = password
        cls.users.append(user)
        return user

    def __init__(self, username=None, email=None, password=None):
        self._username = username
        self._email = email
        self._password = password

    def reset_password(self, resetpassword):
        self.password = resetpassword

    @property
    def username (self):
        return self._username

    @username.setter
    def username(self, value):
        pattern = r'[a-zA-Z]{3,8}'
        match = re.search(pattern, value)
        if match:
            self._username = value
            return 
        assert 0, 'Invalid username'
    
    @property
    def email (self):
        return self._email
    @email.setter
    def email(self, value):
        pattern = r'[a-zA-Z0-9_\.&-]{4,30}@[a-z]+\..'
        match = re.search(pattern, value)
        if match:
            self._email = value
            return 
        assert 0, 'Invalid email'
    
    @property
    def password (self):
        return self._password
    @password.setter
    def password(self, value):
        pattern = r'[a-zA-Z0-9_@&\.]{6,20}'
        match = re.search(pattern, value)
        if match:
            self._password = value
            return 
        assert 0, 'Invalid password'