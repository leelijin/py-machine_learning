from urllib.parse import urljoin

import scrapy
from testspider.items import FirstSpi


class FirstSpider(scrapy.Spider):
    name = 'scdaily'
    allowed_domains = ['opinion.scdaily.cn']
    start_urls = [
        'http://opinion.scdaily.cn/wygz/index.html'
    ]

    def parse(self, response):
        for href in response.css(".sd > sd-box-list > h2 > a::attr('href')"):
            url = urljoin(response.url, href.extract())
            yield scrapy.Request(url, callback=self.parse_content)

    def parse_content(self, response):
        item = FirstSpi()
        item['title'] = response.xpath('//h5/text()').extract_first().strip()
        item['link'] = response.url
        item['img'] = response.xpath('//div[@class="img-box"]/img/@src').extract_first()
        yield item


