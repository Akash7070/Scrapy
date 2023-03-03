import scrapy
from ..items import NewsScrapItem


class NewsSpiderSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = ["www.jagran.com"]
    start_urls = [
        "https://www.jagran.com/news/national-news-hindi.html?itm_medium=national&itm_source=dsktp&itm_campaign=navigation"
        ]
        

    def parse(self, response):
        items = NewsScrapItem()
       
        button_link = response.css('div.pagination.border0 li a::attr(href)').getall()
        button_link = [f'https://www.jagran.com{link}' for link in button_link]
        for link in button_link:
            yield scrapy.Request(link, callback=self.parse_btlink)

        news_links = response.css('ul.topicList li a::attr(href)').getall()
        news_links = [f'https://www.jagran.com{link}' for link in news_links]
        for information in news_links:
                 yield scrapy.Request(information, callback=self.parse_news_info,meta={'news_link': information})

        # items['news_link'] = news_links
        items['button_link'] = button_link
        yield  items


    def parse_btlink(self,response):
            news_links = response.css('ul.topicList li a::attr(href)').getall()
            news_links = [f'https://www.jagran.com{link}' for link in news_links]
            for information in news_links:
                 yield scrapy.Request(information, callback=self.parse_news_info,meta={'news_link': information})

        # Add the extracted links to the item
            items = NewsScrapItem()
            # items['news_link'] = news_links
            
            # yield items

    def parse_news_info(self, response):

        items = NewsScrapItem()
        items['news_link'] = response.meta['news_link']

        #heading of the News
        news_title = response.css('h1::text').extract()

        #image of the News
        news_image = response.css('img::attr(src)').extract()
        for link in news_image:
            if link.startswith("http"):
                pass
            else:
                items['news_image'] = "https:"  + link    #image link stored here
        
        #date of the News
        date = response.css('div.dateInfo span.date::text').extract()
        Publish_date = None
        Updated_date = None
        for item in date:
            if 'Publish Date:' in item:
                Publish_date = item.replace('Publish Date:','').strip()
            elif 'Updated Date:' in item:
                Updated_date = item.replace('Updated Date:','').strip()
            else:
                Publish_date = item
                Updated_date = None

        #paragraph of the News
        paragraphs = []
        paragraph = response.css('.articleBody p::text').getall()
        for para in paragraph:
            paragraphs.append(para)


        # paragraph = response.css('.articleBody p::text').getall()
        # items['paragraph'] = " ".join(paragraph)

        # info = ''.join(paragraphs)
        items['paragraph']= paragraphs
        items['pub_date']=Publish_date
        items['upd_date']=Updated_date
        items['news_title'] = news_title

        yield items

        



        
