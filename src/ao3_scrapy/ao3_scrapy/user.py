# Class for user information

class User(object):
    # Constructor for User object
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.limit = None

    # Set history reading limit
    def set_limit(self, num):
        self.limit = num
