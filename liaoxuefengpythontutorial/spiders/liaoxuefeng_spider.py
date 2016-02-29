import scrapy

from liaoxuefengpythontutorial.items import LiaoxuefengpythontutorialItem

class LiaoxuefengTutorialSpider(scrapy.Spider):
    name = "LiaoxuefengTutorial"
    allowed_domains = ["liaoxuefeng.com"]
    start_urls = [
        "http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="x-sidebar-left-content"]/ul/li/a'):
            #print sel
            #item = LiaoxuefengpythontutorialItem()
            #item['title'] = sel.xpath('text()').extract()
            #item['link'] = sel.xpath('@href').extract()
            #yield item
            #url = sel.xpath('text()').extract()
            href = sel.xpath('@href').extract()
            #print href
            #print "response.url: " + response.url
            newurl = response.urljoin(href[0])
            print newurl
            #url = response.urljoin(sel.xpath('a/@href').extract())
            #print url
            #print href
            yield scrapy.Request(newurl, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
            item = LiaoxuefengpythontutorialItem()
            item['link'] = response.url
            print "item[link]: " + item['link']
            content = response.xpath('//div[@class="x-content"]')
            print content
            item['title'] = content.xpath('h4/text()').extract()
            print item['title']
            #item['desc'] = content.xpath('div[@class="x-wiki-content"]/p/text()').extract()
            item['desc'] = content.xpath('div[@class="x-wiki-content"]//text()').extract()
            print item['desc']
            #item['title'] = response.xpath('content/h4/text()').extract()
            #item['desc'] = response.xpath('conten/div[@class="x-wiki-content"]/text()').extract()
            yield item
