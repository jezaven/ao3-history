import scrapy

def authentication_failed(response):
    if response.xpath('//div[@id="login"]').get() is None:
        return False
    return True

class LoginSpider(scrapy.Spider):
    name = 'login'
    start_urls = ['https://archiveofourown.org/users/login']

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

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed")
        page = response.url.split("/")[-2]
        filename = 'post_login.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        return
