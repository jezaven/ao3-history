# ao3-history
Web scraper for getting story information from user's personal history

You must be have a valid AO3 account and Reading History enabled to use this
---
Running preliminary scrapy

Using terminal, nagivate to ao3_scrapy folder. 

To run scrapy shell to test urls: scrapy shell 'url/to/website'

To run scrapy spider: scrapy crawl [name of spider]

To run scrapy ao3_spider specifically: scrapy crawl history

To run scrapy ao3_spider with json output: scrapy crawl history -o nameoffile.json
