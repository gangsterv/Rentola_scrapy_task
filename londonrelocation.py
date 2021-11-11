import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from property import Property

import re # To keep only numbers from the price


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        # Write your code here and remove `pass` in the following line

        # Extract the data from the HTML response
        titles = response.xpath("//div[@class='h4-space']/h4/a/text()").extract()
        prices = response.xpath("//div[@class='bottom-ic']/h5/text()").extract()
        urls = response.xpath("//div[@class='h4-space']/h4/a/@href").extract()

        # Iterate through the length of the title list since all lists have the same length
        for i in range(len(titles)):
            # Check if the price is per month or week
            if "pw" in prices[i]:
                mult = 4
            else:
                mult = 1
            # an example for adding a property to the json list:    - Create property object and add it to the json file
            property = ItemLoader(item=Property())
            property.add_value('title', titles[i].strip())
            property.add_value('price', str(int(re.sub("[^0-9]", "", prices[i]))) * mult) # Regex substitue any non-digits with empty, then multiply it if needed
            property.add_value('url', 'https://londonrelocation.com'+urls[i])
            yield property.load_item()
