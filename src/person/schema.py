import json


class FriendSchema:
    def __init__(self, person):
        self.id = person.id
        self.first_name = person.first_name
        self.last_name = person.last_name
        self.email = person.email

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)