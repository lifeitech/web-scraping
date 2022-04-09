import scrapy
from douban.items import DoubanItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    start_urls = ('https://movie.douban.com/top250',)

    def parse(self, response):
        li = response.xpath("//ol[@class='grid_view']/li")
        for movie in li:
            doc = DoubanItem()
            doc['rank'] = movie.xpath(".//em/text()")[0].extract()
            doc['title'] = movie.xpath(".//span[@class='title']/text()")[0].extract()
            yield doc

        next_page =response.xpath("//div[@class='paginator']/span[@class='next']/a/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)