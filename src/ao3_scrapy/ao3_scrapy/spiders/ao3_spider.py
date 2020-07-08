# spider to scrape from reading history
import scrapy

# Returns true if login failed
def authentication_failed(response):
    if "The password or user name you entered doesn't match our records".encode() in response.body:
        return True
    return False

class HistorySpider(scrapy.Spider):
    name = "history"

    # Returns iterable of Requests
    def start_requests(self):
        # NOTE: temporary ao3 page before figuring out account authentication
        urls = [
            'https://archiveofourown.org/users/login'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Handles response downloaded from Requests
    def parse(self, response):
        token = response.css('input[name=authenticity_token]::attr(value)').extract_first()

        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'user[login]': 'jeza',
                'user[password]': 'crappypw',
                'authenticity_token' : token
            },
            callback=self.after_login
        )

    # Handles post login response
    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed")
            return
        else:
            return scrapy.Request(
                url='https://archiveofourown.org/users/jeza/readings',
                callback=self.parse_history
            )

    # Extracts works from history pages
    def parse_history(self, response):
        for work in response.css('li.work'):
            # NOTE: href values (urls) can be found using ::attr(href)
            yield {
                'title' : work.css('div.header h4.heading a::text').getall()[0],
                'author' : work.css('div.header h4.heading a::text').getall()[1],
                'fandoms' : work.css('div.header h5.fandoms a::text').getall(),
                'tags' : {
                        'warnings' : work.css('ul.tags li.warnings a.tag::text').getall(),
                        'relationships' : work.css('ul.tags li.relationships a.tag::text').getall(),
                        'characters' : work.css('ul.tags li.characters a.tag::text').getall(),
                        'freeforms' : work.css('ul.tags li.freeforms a.tag::text').getall(),
                    },
                # NOTE: this needs to be reformatted in particular; currently stores as list
                'summary' :  work.css('blockquote.userstuff p::text').getall(),
                'stats' : {
                        'language' : work.css('dl.stats dd.language::text').getall(),
                        # NOTE: this should be reformatted to an int
                        'word_count' : work.css('dl.stats dd.words::text').getall(),
                        # NOTE: chapter_done and chapter_total should be reformatted together
                        'chapter_done' : work.css('dl.stats dd.chapters a::text').getall(),
                        'chapter_total' : work.css('dl.stats dd.chapters::text').getall(),
                        'comments' : work.css('dl.stats dd.comments a::text').getall(),
                        'kudos' : work.css('dl.stats dd.kudos a::text').getall(),
                        'bookmarks' : work.css('dl.stats dd.bookmarks a::text').getall(),
                        'hits' : work.css('dl.stats dd.hits::text').getall()
                    }
            }
