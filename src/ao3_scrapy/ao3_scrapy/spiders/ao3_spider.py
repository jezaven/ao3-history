# spider to scrape from reading history
import scrapy
from ao3_scrapy.account import Account

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

# Converts string representation of numbers to int
def num_convert(num):
    try:
        new = num.replace(',', '')
        return int(new)
    except:
        return num

# Cleans gift data and adds url data for parse_history
def parse_gifted(work):
    users = work.xpath('.//h4/a[contains(@href, "gifts")]/text()').getall()
    urls = work.xpath('.//h4/a[contains(@href, "gifts")]/@href').getall()
    return dict(zip(users, urls))

# Cleans fandom data and adds url data for parse_history
def parse_fandoms(work):
    tags = work.xpath('.//h5/a/text()').getall()
    urls = work.xpath('.//h5/a/@href').getall()
    return dict(zip(tags, urls))

# Cleans warnings data and adds url data for parse_history
def parse_warnings(work):
    tags = work.css('ul.tags li.warnings a.tag::text').getall()
    urls = work.css('ul.tags li.warnings a.tag::attr(href)').getall()
    return dict(zip(tags, urls))

# Cleans relationships data and adds url data for parse_history
def parse_relationships(work):
    tags = work.css('ul.tags li.relationships a.tag::text').getall()
    urls = work.css('ul.tags li.relationships a.tag::attr(href)').getall()
    return dict(zip(tags, urls))

# Cleans characters data and adds url data for parse_history
def parse_characters(work):
    tags = work.css('ul.tags li.characters a.tag::text').getall()
    urls = work.css('ul.tags li.characters a.tag::attr(href)').getall()
    return dict(zip(tags, urls))

# Cleans freeform data and adds url data for parse_history
def parse_freeforms(work):
    tags = work.css('ul.tags li.freeforms a.tag::text').getall()
    urls = work.css('ul.tags li.freeforms a.tag::attr(href)').getall()
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

# Cleans chapter data for parse_history
def parse_chapter(work):
    raw_done = work.css('dl.stats dd.chapters a::text').get()
    raw_total = work.css('dl.stats dd.chapters::text').get()

    try:
        done = int(raw_done)
        total = raw_total[1:]
        if total == '?':
            return [done, -1]
        else:
            return [done, int(total)]
    except:
        return [1, 1]

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
        user = Account('jeza', 'crappypw')
        user.set_limit(3)

        request = scrapy.Request(
            url='https://archiveofourown.org/users/login',
            callback=self.parse,
            cb_kwargs=dict(account=user)
        )

        yield request

    # Handles response downloaded from Requests
    def parse(self, response, account):
        if login_page(response):
            return self.login(response, account)
        else:
            if first_login(response):
                history_page = response.xpath('//a[contains(@href, "readings")]/@href').get()
                return response.follow(
                    url=history_page,
                    callback=self.parse_history,
                    cb_kwargs=dict(account=account)
                )
            else:
                return self.parse_history(response, account)

    # Handles login
    def login(self, response, account):
        token = response.xpath('//input[@name="authenticity_token"]/@value').get()

        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'user[login]': account.username,
                'user[password]': account.password,
                'authenticity_token' : token
            },
            callback=self.after_login,
            cb_kwargs=dict(account=account)
        )

    # Handles post login response
    def after_login(self, response, account):
        if login_page(response):
            self.logger.error("Login failed")
            return
        else:
            return self.parse(response, account)

    # Extracts works from history pages
    def parse_history(self, response, account):
        for work in response.xpath('//li[contains(@id, "work")]'):
            visit = parse_last_visited(work)
            chapter = parse_chapter(work)

            yield {
                'title' : work.xpath('.//h4/a/text()').get(),
                'author' : work.xpath('.//h4/a[@rel="author"]/text()').getall(),
                'gifted' : parse_gifted(work),
                'fandoms' : parse_fandoms(work),
                'tags' : {
                    'ratings' : work.css('ul.required-tags span.rating::attr(title)').get(),
                    'warnings' : parse_warnings(work),
                    'category' : parse_category(work),
                    'completion' : work.css('ul.required-tags span.iswip::attr(title)').get(),
                    'relationships' : parse_relationships(work),
                    'characters' : parse_characters(work),
                    'freeforms' : parse_freeforms(work),
                },
                'series' : {
                    's_title' : work.css('ul.series a::text').get(),
                    'part' : work.css('ul.series strong::text').get(),
                    'url' : work.css('ul.series a::attr(href)').get()
                },
                'summary' : parse_summary(work),
                'stats' : {
                    'language' : work.css('dl.stats dd.language::text').getall(),
                    'word_count' : num_convert(work.css('dl.stats dd.words::text').get()),
                    'chapter_done' : chapter[0],
                    'chapter_total' : chapter[1], # -1 indicated unknown chapter_total
                    'comments' : num_convert(work.css('dl.stats dd.comments a::text').get()),
                    'kudos' : num_convert(work.css('dl.stats dd.kudos a::text').get()),
                    'bookmarks' : num_convert(work.css('dl.stats dd.bookmarks a::text').get()),
                    'hits' : num_convert(work.css('dl.stats dd.hits::text').get())
                },
                'last_visited' : {
                    'date' : visit[0],
                    'version' : visit[1],
                    'count' : visit[2]
                }
            }

        account.update_page()
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None and account.check_limit():
            yield response.follow(
                next_page,
                callback=self.parse,
                cb_kwargs=dict(account=account)
            )
