# Class for user information

class Account(object):
    # Constructor for User object
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.limit = None
        self.pages = 0

    # Set history reading limit
    def set_limit(self, num):
        self.limit = num

    # Update pages scraped
    def update_page(self):
        self.pages = self.pages + 1

    # Check if pages met limit
    def check_limit(self):
        return self.pages < self.limit
