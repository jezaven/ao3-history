# Class for work information

class Work(object):
    # Constructor for User object
    def __init__(self):
        self.id = None
        self.url = None
        self.title = ""
        self.authors = None
        self.gifted = ""
        self.fandoms = None

        # tags
        self.ratings = None
        self.warnings = None
        self.categories = None
        self.completion = ""
        self.relationships = None
        self.characters = None
        self.freeforms = None

        # series
        self.series_title = None
        self.series_part = None
        self.series_url = None

        self.summary = None

        # stats
        self.language = ""
        self.word_count = None
        self.chapter_done = None
        self.chapter_total = None
        self.comments = None
        self.kudos = None
        self.bookmarks = None
        self.hits = None

        # last visited
        self.last_visit_date = None
        self.last_visit_version = None
        self.last_visit_count = None

    # Set fic id and url
    def set_id(self, id):
        self.id = id
        self.url = "https://archiveofourown.org/works/" + str(id)
