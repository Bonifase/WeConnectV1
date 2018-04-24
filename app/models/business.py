import re


class Business:
    businesses = []

    class_counter = 1

    @classmethod
    def register_business(cls, name, category, location,userid):
        business = cls()
        business.name = name
        business.category = category
        business.location = location
        business.userid = userid
        business.id = Business.class_counter
        cls.businesses.append(business)
        Business.class_counter += 1
        return business

    def __init__(self, name=None, category=None, location=None, userid =None):
        self._name = name
        self._category = category
        self._location = location
        self.userid = userid


    def update_business(self, data, issuer_id):
        # data  is a dict
        if issuer_id == self.userid:
            for key in data.keys():
                value = data[key]
                setattr(self, key, value)
        else:
            assert 0, 'This business is registered to another user'


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

