
class Vendor:
    def __init__(self, token, name):
        self.token = token
        self.name = name

    def __lt__(self, other):
        return self.token < other.token
