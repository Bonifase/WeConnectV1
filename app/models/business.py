import re


class Business:
    businesses = []

    class_counter = 1

    @classmethod
    def register_business(cls, name, category, location):
        business = cls()
        business.name = name
        business.category = category
        business.location = location
        business.id = Business.class_counter
        cls.businesses.append(business)
        Business.class_counter += 1
        return business

    def __init__(self, name=None, category=None, location=None):
        self._name = name
        self._category = category
        self._location = location

    def update_business(self, newname, newcategory, newlocation):
        self.name = newname
        self.category = newcategory
        self.location = newlocation

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        pattern = r'[a-zA-Z\. ]{3,10}'
        match = re.search(pattern, value)
        if match:
            self._name = value
            return
        assert 0, 'Invalid name'

    @property
    def newname(self):
        return self._name

    @newname.setter
    def newname(self, value):
        pattern = r'[a-zA-Z\. ]{3,10}'
        match = re.search(pattern, value)
        if match:
            self._name = value
            return
        assert 0, 'Invalid name'
