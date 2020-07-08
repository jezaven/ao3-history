import scrapy

class LoginSpider(scrapy.Spider):
    name = 'login'

    def authentication_failed(response):
        pass

    def start_requests(self):
        urls = [
            'http://www.example.com/users/login.php'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            reponse,
            formdata={
                'user[name]' : 'john',
                'user[pw]' : 'secret',
            },
            callback=self.after_login(response)
        )

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed")
            return
