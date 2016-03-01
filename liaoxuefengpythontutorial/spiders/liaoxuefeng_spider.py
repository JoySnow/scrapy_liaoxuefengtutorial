import scrapy
import re

from liaoxuefengpythontutorial.items import LiaoxuefengpythontutorialItem

class LiaoxuefengTutorialSpider(scrapy.Spider):
    name = "LiaoxuefengTutorial"
    allowed_domains = ["liaoxuefeng.com"]
    start_urls = [
        "http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/"
    ]

    def parse(self, response):
        level_index = [0, 0, 0, 0]  #to number the pages in turn, for storing
        for sel in response.xpath('//div/ul[@style="margin-right:-15px;"]/li'):
            #print sel
            title_index = ""  #will be put before title as index
            style = sel.xpath('@style').extract()  #index by style="margin-left:*em;"
            if style:  #the normal ones, as "*.*.*." for the longest
                match_res = re.match(r'margin-left:([0-9]*)em', style[0])
                if match_res:
                    margin_left = int(match_res.group(1))
                    #print "match_res.group(1): " + match_res.group(1)
                    level_index[margin_left] += 1
                    level = margin_left + 1
                    while level <= 3:  #after ++, the tails will be removed
                        level_index[level] = 0
                        level += 1
                    level = 1
                    while level <= margin_left:  #append to title_index
                        title_index += str(level_index[level]) + '.'
                        level += 1
                    title_index += ' '
            else:  #the first one is special, as "0." now.
                title_index = "0. "
            #print title_index
            # title_index part is done.
            item = LiaoxuefengpythontutorialItem()
            #print sel.xpath('a/text()').extract()
            #item['title'] = sel.xpath('a/text()').extract()
            item['title'] = title_index + sel.xpath('a/text()').extract()[0]
            #print item['title']
            item['link'] = sel.xpath('a/@href').extract()

            #yield item
            #url = sel.xpath('text()').extract()
            #href = sel.xpath('@href').extract()
            #print href
            #print "response.url: " + response.url
            newurl = response.urljoin(item['link'][0])
            #print "newurl: " + newurl
            #url = response.urljoin(sel.xpath('a/@href').extract())
            #print url
            #print href
            request = scrapy.Request(newurl, callback=self.parse_dir_contents)
            request.meta['item'] = item
            yield request
            #yield item

    def parse_dir_contents(self, response):
            #item = LiaoxuefengpythontutorialItem()
            item = response.meta['item']
            #item['link'] = response.url
            #print "item[link]: " + item['link']
            content = response.xpath('//div[@class="x-content"]')
            print content
            #item['title'] = content.xpath('h4/text()').extract()
            #print item['title']
            #item['desc'] = content.xpath('div[@class="x-wiki-content"]/p/text()').extract()
            item['desc'] = content.xpath('div[@class="x-wiki-content"]//text()').extract()
            print item['desc']
            #item['title'] = response.xpath('content/h4/text()').extract()
            #item['desc'] = response.xpath('conten/div[@class="x-wiki-content"]/text()').extract()
            yield item
