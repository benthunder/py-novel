import scrapy
import json
import re


class DaoquanSpider(scrapy.Spider):
    name = "daoquan"
    allowed_domains = ["daoquan.vn"]
    start_urls = [
        # "https://daoquan.vn/dich-chang-re-manh-nhat-lich-su/371/1/chuong-1"
    ]
    slug = "chang-re-manh-nhat-lich-su"
    novel_data = {}

    def __init__(self, *args, **kwargs):
        super(DaoquanSpider, self).__init__(*args, **kwargs)
        self.start_urls = self.getUrlsFromJson()

    def parse(self, response):
        content = response.css(".content-chapter-mobile").get()
        title = response.css(".chapter-title::text").get()
        novel_chapter_match = (
            re.search(r"chuong-(\d+)", response.url) if response.url else None
        )

        novel_chapter_number = (
            novel_chapter_match.group(1) if novel_chapter_match else None
        )
        self.novel_data[novel_chapter_number]["content"] = content

        yield {
            "title": title,
            "content": content,
        }

    def getUrlsFromJson(self):
        urls = {}
        with open(
            "../novel/chang-re-manh-nhat-lich-su.json", "r", encoding="utf-8"
        ) as json_file:
            listUrlData = json.load(json_file)
        for urlData in listUrlData:
            urls[urlData["chapter"]] = {
                "url": urlData["url"],
                "title": urlData["title"],
            }
        self.novel_data = urls
        finalListUrl = [chapter["url"] for chapter in urls.values()]
        return finalListUrl[::-1]
