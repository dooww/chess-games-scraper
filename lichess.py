import scrapy
import logging
# import pprint
from scrapy.http import FormRequest
# from scrapy_splash import SplashRequest ,SplashFormRequest
# from scrapy_scrapingbee import ScrapingBeeSpider, ScrapingBeeRequest


# chess games scraper class
class ChessGamesScraper(scrapy.Spider):
    # spider name
    name = 'lichess'

    # base url
    base_url = 'https://lichess.org/@/hediiiiiii/search'
    login_url='https://lichess.org/login'

    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    # start crawling
    def start_requests(self):
        # lichess specific API key
        key_id = 1584694629328

        # loop over pages
        for page in range(1, 50):   # set max pages up to 1500 up to
            next_page = self.base_url + '?page=' + str(page) + '&perf=2&sort.field=d&sort.order=desc&_=' + str(key_id)
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse_game_list)
            key_id += 1

    # parse game list
    def parse_game_list(self, res):
        # extract game links
        games = res.css('a.game-row__overlay::attr(href)').getall()

        # loop over game links
        for game in games:
            yield res.follow(url=game, headers=self.headers, callback=self.parse_game)

    # parse game
    def parse_game(self, res):
        # extract PGN game
        pgn = res.css('div.pgn::text').get()

        # write PGN game to file
        # (PGN) is the most popular standard for the representation of chess games
        with open('kingscrusher.pgn', 'a') as f:
            f.write(pgn + '\n\n\n')

    #login method to allow  us  to get  all the games from lichess
    def parse_login_lichess(self, response):
        return scrapy.FormRequest(
            url=self.login_url,
            headers=self.headers,
            formdata={'username': 'Hediiiiiii', 'password': '*********'},
            callback=self.after_login
         )

    def after_login(self, response):
        # if (response.url='https://lichess.org'):
        #     print('*******************************  Doneeeee  ******************************')
            if "Error while logging in" in str(response.body):
                self.logger.error("Login failed!")
            else:
                self.logger.error("Login succeeded!")
                yield  response
FormRequest("INSERT URL", formdata={"user":"user",  "pass":"pass"}, callback=self.parse)]
