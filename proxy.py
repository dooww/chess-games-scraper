import scrapy
from scrapy_splash import SplashRequest
from scrapy_scrapingbee import ScrapingBeeSpider, ScrapingBeeRequest


class ProxySpider(scrapy.Spider):
    header={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    name = 'proxy'
    start_urls = ['https://free-proxy-list.net/']
    youtubevideo='https://www.youtube.com/watch?v=ps9VFsgSj4k'
    def parse(self, response):
        proxy_list=[]
        #extract all the proxy
        list1=response.css('#proxylisttable td:nth-child(2)::text ').getall()
        list2=response.css(' #proxylisttable td:nth-child(1)::text').getall()
        for x in range(len(list1)):
            proxy='https://' + list2[x] + ':' + list1[x]
            proxy_list.append(proxy)
            #make use for those proxy  by adding view on youtube
            yield scrapy.Request(url=self.youtubevideo,callback=self.parse_view,headers=self.header,meta={"proxy": proxy})
    def parse_view(self,response):
        print('******************************* done **********************************')

        # rows=response.css('#proxylisttable td')
        # for row in rows:
        # 	yield{'adressip': row.css('a::text').get(),
        # 			'port': row.css('td:nth-child(1)::text').get() ,
        # 			'country' : row.css('td:nth-child(4)::text').get(),
        # 			'https' : row.css('td:nth-child(7)::text').get()
        # 	}
