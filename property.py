import scrapy
from itemloaders.processors import Join


class Property(scrapy.Item):
    title = scrapy.Field(output_processor=Join())
    price = scrapy.Field(output_processor=Join())

    # The url part gave an error, so I added it here
    url = scrapy.Field(output_processor=Join())
