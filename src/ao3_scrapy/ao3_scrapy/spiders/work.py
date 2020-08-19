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
        self.summary = None

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

    # Set fic title
    def set_title(self, title):
        self.title = title

    # Set fic authors
    def set_authors(self, authors):
        self.authors = authors

    # Set fic gifted
    def set_gifted(self, gifted):
        self.gifted = gifted

    # Set fic fandoms
    def set_fandoms(self, fandoms):
        self.fandoms = fandoms

    # Set fic summary
    def set_summary(self, summary):
        self.summary = summary

    # Set fic ratings
    def set_ratings(self, ratings):
        self.ratings = ratings

    # Set fic warnings
    def set_warnings(self, warnings):
        self.warnings = warnings

    # Set fic categories
    def set_categories(self, categories):
        self.categories = categories

    # Set fic completion
    def set_completion(self, completion):
        self.completion = completion

    # Set fic relationships
    def set_relationships(self, relationships):
        self.relationships = relationships

    # Set fic characters
    def set_characters(self, characters):
        self.characters = characters

    # Set fic freeforms
    def set_freeforms(self, freeforms):
        self.freeforms = freeforms

    # Set fic series_title
    def set_series_title(self, series_title):
        self.series_title = series_title

    # Set fic authors
    def set_series_part(self, series_part):
        self.series_part = series_part

    # Set fic series_url
    def set_series_url(self, series_url):
        self.series_url = series_url

    # Set fic language
    def set_language(self, language):
        self.language = language

    # Set fic word_count
    def set_word_count(self, word_count):
        self.word_count = word_count

    # Set fic chapter_done
    def set_chapter_done(self, chapter_done):
        self.chapter_done = chapter_done

    # Set fic chapter_total
    def set_chapter_total(self, chapter_total):
        self.chapter_total = chapter_total

    # Set fic comments
    def set_comments(self, comments):
        self.comments = comments

    # Set fic kudos
    def set_kudos(self, kudos):
        self.kudos = kudos

    # Set fic
    def set_bookmarks(self, bookmarks):
        self.bookmarks = bookmarks

    # Set fic hits
    def set_hits(self, hits):
        self.hits = hits

    # Set fic last_visit_date
    def set_last_visit_date(self, last_visit_date):
        self.last_visit_date = last_visit_date

    # Set fic last_visit_version
    def set_last_visit_version(self, last_visit_version):
        self.last_visit_version = last_visit_version

    # Set fic last_visit_count
    def set_last_visit_count(self, last_visit_count):
        self.last_visit_count = last_visit_count

    def get_json(self):
        data = {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'authors': self.authors,
            'gifted': self.gifted,
            'fandoms': self.fandoms,
            'summary': self.summary,
            'tags': {
                'ratings': self.ratings,
                'warnings': self.warnings,
                'categories': self.categories,
                'completion': self.completion,
                'relationships': self.relationships,
                'characters': self.characters,
                'freeforms': self.freeforms,
            },
            'series': {
                'series_title': self.series_title,
                'series_part': self.series_part,
                'series_url': self.series_url,
            },
            'stats': {
                'language': self.language,
                'word_count': self.word_count,
                'chapter_done': self.chapter_done,
                'chapter_total': self.chapter_total,
                'comments': self.comments,
                'kudos': self.kudos,
                'bookmarks': self.bookmarks,
                'hits': self.hits,
            },
            'last_visited': {
                'date': self.last_visit_date,
                'version': self.last_visit_version,
                'count': self.last_visit_count,
            }
        }
        return data
