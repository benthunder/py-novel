# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NovelPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=spider.settings.get("MYSQL_HOST"),
            port=spider.settings.get("MYSQL_PORT"),
            user=spider.settings.get("MYSQL_USER"),
            password=spider.settings.get("MYSQL_PASSWORD"),
            database=spider.settings.get("MYSQL_DB"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        
        return item
