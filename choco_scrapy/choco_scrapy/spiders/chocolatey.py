import scrapy
import json
from scrapy.loader import ItemLoader
from amazon_scrapy.items import ChocolateyItem


class ChocolateySpider(scrapy.Spider):
    name = 'chocolatey'
    custom_settings = {
        "FEEDS": {
            name + ".json": {
                "format": "json",
                "encoding": "utf8",
                "store_empty": False
            }
        },
        "LOG_LEVEL": "INFO",
    }
    allowed_domains = ['chocolatey.org']

    with open('applist.txt', 'r') as a:
        appslist = [s.replace(' ', '+') for s in a.read().splitlines()]

    start_urls = [
        f'https://community.chocolatey.org/packages?q={query}' for query in appslist
    ]

    def parse(self, response):
        self.logger.info(
            f'url: {response.url}\nstatus code: {str(response.status)}')

        if (response.status == 200):

            try:
                apps = response.css('.package-list-view > li')
                print(len(apps))
            except:
                self.logger.info('error getting apps')

            try:
                for app in apps:
                    print(app.css('a.h5::text').get())
                    chocoLoader = ItemLoader(item=ChocolateyItem())
                    chocoLoader.add_value('name', app.css('a.h5::text').get())
                    chocoLoader.add_value(
                        'link', app.css('a.h5::attr(href)').get())
                    chocoLoader.add_value(
                        'code', app.css('input::attr(value)').get())
                    chocoLoader.add_value('downloads', app.css(
                        '.rounded-pill::text').get())

                    yield chocoLoader.load_item()

            except:
                self.logger.info('error looping apps')
