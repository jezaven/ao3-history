# spider to scrape from reading history
import scrapy

class WorkSpider(scrapy.Spirder):
    name = "works"

    # Returns iterable of Requests
    def start_requests(self):
        # NOTE: temporary ao3 page before figuring out account authentication
        urls = [
            'https://archiveofourown.org/tags/The%20Good%20Place%20(TV)/works?page=1',
            'https://archiveofourown.org/tags/The%20Good%20Place%20(TV)/works?page=2'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Handles response downloaded from Requests
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
