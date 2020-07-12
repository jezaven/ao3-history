# Class for user information

class Account(object):
    # Constructor for User object
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.limit = None
        self.pages = 0

    # Set history page limit
    def set_limit(self, num):
        self.limit = num

    # Update pages scraped
    def update_page(self):
        self.pages = self.pages + 1

    # Returns True if page limit not met
    def check_limit(self):
        if self.limit is not None:
            return self.pages < self.limit
        else:
            return True
