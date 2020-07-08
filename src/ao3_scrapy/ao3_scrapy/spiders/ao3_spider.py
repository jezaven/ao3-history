# spider to scrape from reading history
import scrapy

class WorkSpider(scrapy.Spider):
    name = "works"

    # Returns iterable of Requests
    def start_requests(self):
        # NOTE: temporary ao3 page before figuring out account authentication
        urls = [
            'https://archiveofourown.org/tags/The%20Good%20Place%20(TV)/works?page=1',
            'https://archiveofourown.org/tags/%E3%83%A2%E3%83%96%E3%82%B5%E3%82%A4%E3%82%B3100%20%7C%20Mob%20Psycho%20100/works'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Handles response downloaded from Requests
    def parse(self, response):
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
