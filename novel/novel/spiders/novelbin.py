import scrapy
import json
import re
import sys


class NovelbinSpider(scrapy.Spider):
    name = "novelbin"
    allowed_domains = ["novelbin.com"]
    start_urls = []
    slug = "absolute-sword-sense"
    title = "Tuyệt đối kiếm cảm"
    novel_data = {}

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://novelbin.com/ajax/chapter-archive?novelId=absolute-sword-sense",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    }

    cookies = {
        "_ga": "GA1.1.1029526527.1739389877",
        "_sharedID": "bc09a410-2dc0-45bb-be3e-2214b08d2a7a",
        "cf_clearance": "QcSglathG1NsvUhK247iaSP9oTAFKQeeNbQH2ByXE1Y-1740017713-1.2.1.1-ePQuAxjfe5kWL0yC_oxJtFgdA7q3qj6fL7V5B_BK8C4LBOsRpktmWnhsY2v5r51k4iAbgAshzu8bXepM_QzlRxXf00vNaDOocqI6nulcSqk4DK3Cd6CqLjN6nUiIWPtA4FM_21gpuLiZr38iP8oaRONWSDbkR7DWCJ77ttfzyddXveKwoVS5Yt6Kyvj6zGfXuElsXvUIsElrV.M.ZcTZleZnnbfXOldmNsGZ3qeh7IGv7H1b_kTpIeCUqjp2sFEMTmtSYM_LP7T_tVmHgLAQ9E2sUSoEHzQI5CW9k1UtY.h380Nxj.LMLEH61BDaIuOvhqJi4HrRzYx4.IML21tGJw",
    }

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": headers,
        # "DOWNLOAD_DELAY": 1,
        "COOKIES_ENABLED": True,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    }

    def __init__(self, *args, **kwargs):
        super(NovelbinSpider, self).__init__(*args, **kwargs)
        self.start_urls = self.getUrlsFromJson()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url, cookies=self.cookies, callback=self.parse, headers=self.headers
            )

    def parse(self, response):
        content = response.css("#chr-content").get()
        title = response.css(".chr-title >span::text").get().strip()
        yield {
            "title": title,
            "content": content,
        }

    def getUrlsFromJson(self):
        urls = {}
        with open(f"../novel/{self.slug}.json", "r", encoding="utf-8") as json_file:
            listUrlData = json.load(json_file)
        for urlData in listUrlData:
            urls[urlData["chapter"]] = {
                "url": urlData["url"],
                "title": urlData["title"],
                "chapter": urlData["chapter"],
            }
        self.novel_data = urls
        finalListUrl = [chapter["url"] for chapter in urls.values()]
        return finalListUrl[::-1]
