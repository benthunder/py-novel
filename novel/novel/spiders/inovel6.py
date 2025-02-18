import scrapy
import json
import re


class Inovel6Spider(scrapy.Spider):
    name = "inovel6"
    allowed_domains = ["inovel6.com"]
    start_urls = [
        # "https://inovel6.com/mao-son-troc-quy-nhan/chuong-386-ran-doc-phan-1-616cf4261868223e632a8876.html"
    ]
    slug = "mao-son-troc-quy-nhan"
    novel_data = {}

    def __init__(self, *args, **kwargs):
        super(Inovel6Spider, self).__init__(*args, **kwargs)
        self.start_urls = self.getUrlsFromJson()

    def parse(self, response):
        content = response.css("#showContent").get()
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
            "../novel/mao-son-troc-quy-nhan.json", "r", encoding="utf-8"
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
