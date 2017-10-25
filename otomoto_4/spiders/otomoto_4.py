import scrapy
from otomoto_4.items import Otomoto4Item


class Otomoto4(scrapy.Spider):
    name = 'otomoto4'
    allowed_domains = ['www.otomoto.pl']
    start_urls = ['https://www.otomoto.pl/osobowe/']

    def parse(self, response):

        # create array of auctions links
        auctions = response.xpath('//h2[@class="offer-title"]/a/@href').extract()

        for auction in auctions:

            # define item
            item = Otomoto4Item()

            # add link to auction
            item['link'] = auction
            item['parameters'] = {}
            
            # pass each page to the parse_auction() method
            request = scrapy.Request(auction, callback=self.parse_auction)
            request.meta['item'] = item

            # add item to array of items
            yield request

        for li in response.css('li.next a'):
            yield response.follow(li, callback=self.parse)

    def parse_auction(self, response):
        item = response.meta['item']

        items = response.xpath('//*[@class="offer-params__item"]')

        for row in items:

            item['parameters'][row.xpath('span/text()').extract_first()] = row.xpath('div/a/@title').extract_first()

        yield item
