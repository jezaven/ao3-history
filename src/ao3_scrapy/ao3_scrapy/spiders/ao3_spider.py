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
        'Jan' : 1,
        'Feb' : 2,
        'Mar' : 3,
        'Apr' : 4,
        'May' : 5,
        'Jun' : 6,
        'Jul' : 7,
        'Aug' : 8,
        'Sep' : 9,
        'Oct' : 10,
        'Nov' : 11,
        'Dec' : 12
    }
    return convert[mon]

# Cleans fandom data for parse_history
def parse_fandoms(work):
    tags = work.xpath('.//h5/a/text()').getall()
    urls = work.xpath('.//h5/a/@href').getall()
    return dict(zip(tags, urls))

# Cleans category data for parse_history
def parse_category(work):
    raw = work.css('ul.required-tags span.category::attr(title)').get()
    return raw.split(', ')

# Cleans summary data for parse_history
def parse_summary(work):
    raw = work.xpath('.//blockquote[@class="userstuff summary"]//text()').getall()

    for i in range(len(raw)):
        raw[i] = raw[i].strip('\n ')

    raw_new = list(filter(None, raw))
    return ''.join(raw)

# Cleans last visited data for parse_history
def parse_last_visited(work):
    raw = work.css('h4.viewed::text').getall()
    all_clean = raw[1].strip()
    all_stats = all_clean.split('\n\n          ')

    # Clean date
    temp_date = all_stats[0].split()
    all_stats[0] = {
        'day' : int(temp_date[0]),
        'month' : month_convert(temp_date[1]),
        'year' : int(temp_date[2])
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
    # NOTE: improve non-english characters
    # NOTE: add gifted fic
    # NOTE: change empty stats to 0
    # NOTE: convert numbers to int
    def parse_history(self, response):
        for work in response.xpath('//li[contains(@id, "work")]'):
            fandoms = parse_fandoms(work)
            category = parse_category(work)
            summary = parse_summary(work)
            visit = parse_last_visited(work)

            yield {
                'title' : work.xpath('.//h4/a/text()').get(),
                'author' : work.xpath('.//h4/a[@rel="author"]/text()').getall(),
                'fandoms' : fandoms,
                'tags' : {
                    'ratings' : work.css('ul.required-tags span.rating::attr(title)').get(),
                    'warnings' : work.css('ul.required-tags span.warnings::attr(title)').getall(),
                    'category' : category,
                    'completion' : work.css('ul.required-tags span.iswip::attr(title)').get(),
                    'relationships' : work.css('ul.tags li.relationships a.tag::text').getall(),
                    'characters' : work.css('ul.tags li.characters a.tag::text').getall(),
                    'freeforms' : work.css('ul.tags li.freeforms a.tag::text').getall(),
                },
                'series' : {
                    's_title' : work.css('ul.series a::text').get(),
                    'part' : work.css('ul.series strong::text').get(),
                    'url' : work.css('ul.series a::attr(href)').get()
                },
                'summary' :  summary,
                'stats' : {
                    'language' : work.css('dl.stats dd.language::text').getall(),
                    # NOTE: this should be reformatted to an int
                    'word_count' : work.css('dl.stats dd.words::text').get(),
                    # NOTE: chapter_done and chapter_total should be reformatted together
                    'chapter_done' : work.css('dl.stats dd.chapters a::text').get(),
                    'chapter_total' : work.css('dl.stats dd.chapters::text').get(),
                    'comments' : work.css('dl.stats dd.comments a::text').get(),
                    'kudos' : work.css('dl.stats dd.kudos a::text').get(),
                    'bookmarks' : work.css('dl.stats dd.bookmarks a::text').get(),
                    'hits' : work.css('dl.stats dd.hits::text').get()
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
