import scrapy
#from scrapy.crawler import CrawlerProcess
import re


from liaoxuefengpythontutorial.items import LiaoxuefengpythontutorialItem


class LiaoxuefengProgrammingSpider(scrapy.Spider):
    name = "LiaoxuefengProgramming"
    start_urls = [
        "http://www.liaoxuefeng.com/category/0013738748415562fee26e070fa4664ad926c8e30146c67000"
    ]

    def parse(self, response):
        page_sum = int(response.xpath('//ul[@class="uk-pagination"]/li[last()]/a/text()').extract()[0])
        url = response.url + "?page="
        print url
        for index in range(1, page_sum+1):
            newurl = url + str(index)
            request = scrapy.Request(newurl, callback=self.parse_page_contents)
            yield request
        #print page_sum
        #print page_sum.extract()

    def parse_page_contents(self, response):
        for sel in response.xpath('//div[@class="x-content"]/div'):
            content = sel.xpath('div[1]/h3/a')
            print content
            item = LiaoxuefengpythontutorialItem()
            #print sel.xpath('a/text()').extract()
            #item['title'] = sel.xpath('a/text()').extract()
            item['title'] = content.xpath('text()').extract()
            print item['title']
            item['link'] = content.xpath('@href').extract()
            newurl = response.urljoin(item['link'][0])
            #newurl = item['link'][0]
            print newurl
            item['link'][0] = newurl
            request = scrapy.Request(newurl, callback=self.parse_dir_contents)
            request.meta['item'] = item
            yield request
            #yield item

    def parse_dir_contents(self, response):
        item = response.meta['item']
        item['desc'] = response.xpath('//div[@class="x-article-content"]//text()').extract()
        yield item







