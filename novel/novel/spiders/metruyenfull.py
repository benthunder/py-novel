import scrapy
import json
import re


class MetruyenfullSpider(scrapy.Spider):
    name = "metruyenfull"
    allowed_domains = ["metruyenfull.org"]
    start_urls = [
        # "https://metruyenfull.org/chang-re-manh-nhat-lich-su/chuong-683-tot-dep-dai-ket-cuc.html"
    ]
    slug = "chang-re-manh-nhat-lich-su"
    novel_data = {}

    def __init__(self, *args, **kwargs):
        super(MetruyenfullSpider, self).__init__(*args, **kwargs)
        self.start_urls = self.getUrlsFromJson()

    def parse(self, response):
        content = response.css("#chapter-c").get()
        title = response.css(".chapter-title > .chapter-text > span::text").get()
        novel_chapter_match = (
            re.search(r"chuong-(\d+)", response.url) if response.url else None
        )

        novel_chapter_number = (
            novel_chapter_match.group(1) if novel_chapter_match else None
        )
        self.novel_data[novel_chapter_number] = {}
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
