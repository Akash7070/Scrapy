# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class NewsScrapPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    #create dbase connection
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'Scrapping'
        )
        self.curr = self.conn.cursor()

    #Table creation
    def create_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS Scrap_News(
                          id INT AUTO_INCREMENT PRIMARY KEY, 
                          news_link VARCHAR(255), 
                          news_title VARCHAR(255), 
                          news_image VARCHAR(255), 
                          paragraph TEXT , 
                          pub_date VARCHAR(255), 
                          upd_date VARCHAR(255))""")
        
    #storing the data
    def store_db(self,news_link_str,news_title_str, news_image_str, paragraphs_str, pub_date_str, upd_date_str):
        self.curr.execute("""INSERT INTO Scrap_News (id, news_link, news_title, news_image, paragraph, pub_date, upd_date) VALUES(NULL, %s, %s, %s, %s, %s, %s)""",(
            news_link_str,
            news_title_str,
            news_image_str, 
            paragraphs_str, 
            pub_date_str, 
            upd_date_str
        ))
        self.conn.commit()
    

    def process_item(self, item, spider):

        news_link = item['news_link']
        news_link_str = ''.join(news_link)

        news_title = item['news_title']
        news_title_str = ''.join(news_title)

        news_image = item['news_image']
        news_image_str = ''.join(news_image)
        
        paragraphs = item['paragraph']
        paragraphs_str = ''.join(paragraphs)  # Join paragraphs with separator

        pub_date = item['pub_date']
        pub_date_str = ''.join(pub_date)

        upd_date = item['upd_date']
        upd_date_str = ''.join(upd_date)


        self.store_db(news_link_str,news_title_str, news_image_str, paragraphs_str, pub_date_str, upd_date_str)
        return item
