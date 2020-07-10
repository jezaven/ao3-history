# spider to scrape from reading history
import scrapy

# Returns True if it is the login page
def login_page(response):
    if "Log in".encode() in response.body:
        return True
    return False

# Returns True if it is the first login attempt
def first_login(response):
    if "History" == response.xpath('//h2[@class="heading"]/text()').get():
        return False
    else:
        return True

# Converts string representation of month to int
def month_convert(mon):
    convert = {
        'Jan' : '01',
        'Feb' : '02',
        'Mar' : '03',
        'Apr' : '04',
        'May' : '05',
        'Jun' : '06',
        'Jul' : '07',
        'Aug' : '08',
        'Sep' : '09',
        'Oct' : '10',
        'Nov' : '11',
        'Dec' : '12'
    }
    return convert[mon]

# Cleans last visited data for parse_history
def parse_last_visited(work):
    raw = work.css('h4.viewed::text').getall()
    all_clean = raw[1].strip()
    all_stats = all_clean.split('\n\n          ')

    # Clean date
    temp_date = all_stats[0].split()
    all_stats[0] = {
        'day' : temp_date[0],
        'month' : month_convert(temp_date[1]),
        'year' : temp_date[2]
    }

    # Clean version information
    all_stats[1] = all_stats[1].strip('().')

    # Clean visit count
    try:
        all_stats[2] = int(all_stats[2].split()[1])
    except:
        all_stats[2] = 1

    return all_stats

class HistorySpider(scrapy.Spider):
    name = "history"

    # Returns iterable of Requests
    def start_requests(self):
        urls = [
            'https://archiveofourown.org/users/login'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Handles response downloaded from Requests
    def parse(self, response):
        if login_page(response):
            return self.login(response)
        else:
            if first_login(response):
                history_page = response.xpath('//a[contains(@href, "readings")]/@href').get()
                return response.follow(url=history_page, callback=self.parse_history)
            else:
                return self.parse_history(response)

    # Handles login
    # NOTE: need to make user class to path login information from
    def login(self, response):
        token = response.xpath('//input[@name="authenticity_token"]/@value').get()

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
        if login_page(response):
            self.logger.error("Login failed")
            return
        else:
            return self.parse(response)

    # Extracts works from history pages
    # NOTE: add series field
    # NOTE: improve non-english characters
    # NOTE: add gifted fic
    def parse_history(self, response):
        for work in response.xpath('//li[contains(@id, "work")]'):
            visit = parse_last_visited(work)

            yield {
                'title' : work.xpath('.//h4/a/text()').get(),
                'author' : work.xpath('.//h4/a[@rel="author"]/text()').getall(),
                'fandoms' : work.xpath('.//h5/a/text()').getall(),
                'tags' : {
                    'ratings' : work.css('ul.required-tags span.rating::attr(title)').get(),
                    'warnings' : work.css('ul.required-tags span.warnings::attr(title)').getall(),
                    # NOTE: multiple categories stored as one element
                    'category' : work.css('ul.required-tags span.category::attr(title)').get(),
                    'completion' : work.css('ul.required-tags span.iswip::attr(title)').get(),
                    'relationships' : work.css('ul.tags li.relationships a.tag::text').getall(),
                    'characters' : work.css('ul.tags li.characters a.tag::text').getall(),
                    'freeforms' : work.css('ul.tags li.freeforms a.tag::text').getall(),
                },
                'series' : {
                    's_title' : work.css('ul.series a::text').getall(),
                    'part' : work.css('ul.series strong::text').getall(),
                    'url' : work.css('ul.series a::attr(href)').getall()
                },
                # NOTE: needs to be fixed, see call me beep me
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
                },
                'last_visited' : {
                    'date' : visit[0],
                    'version' : visit[1],
                    'count' : visit[2]
                }
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
