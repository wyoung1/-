import scrapy
from ..items import LianjiaItem
import re
page = 100
areas = ['dongcheng', 'xicheng', 'haidian', 'chaoyang']


class GethouseSpider(scrapy.Spider):
    name = 'gethouse'
    # allowed_domains = ['www.xxx.com']
    start_urls = []
    for area in areas:
        for i in range(1, page+1):
            start_urls.append('https://bj.lianjia.com/zufang/{}/pg{}/'.format(area, i))

    def parse(self, response):
        item = LianjiaItem()
        div_list = response.xpath('//div[@class="content__list"]/div')
        for div in div_list:
            item['name'] = div.xpath('.//a[@class="content__list--item--aside"]/@title').extract()[0].split(' ')[0]
            item['house_type'] = div.xpath('.//a[@class="content__list--item--aside"]/@title').extract()[0].split(' ')[1]
            item['price'] = div.xpath('.//span[@class="content__list--item-price"]//text()').extract()[0]
            item['area'] = div.xpath('.//p[@class="content__list--item--des"]/a[1]/text()').extract()[0]
            temp = div.xpath('.//p[@class="content__list--item--des"]//text()').extract()
            item['acreage'] = re.findall('/\n        (.*?)㎡', ''.join(temp), re.S)[0]
            print('完成一页')
            yield item
