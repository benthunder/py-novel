import scrapy
import json
import re
import sys


class NovelbinSpider(scrapy.Spider):
    name = "novelbin"
    allowed_domains = ["novelbin.com"]
    start_urls = []
    slug = "nano-machine-retranslated-version"
    title = "Tuyệt đối kiếm cảm"
    novel_data = {}

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://novelbin.com/ajax/chapter-archive?novelId=nano-machine-retranslated-version",
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
        "cf_clearance": "KTDoOq8GZgEd7sh.dXuTKImwidNwnEXSzFdab.UNFhs-1740050734-1.2.1.1-.MK15AQQF6JMBTrl0hhd43hNhOa0..uXFbMuhhnY.qX39kwCrQkKWSZM7CmSc4WCKAhBsWPWAnTLHDzW5OCPt4kw3ggey3.ptTIdLpL6B0tY566OllJUkdiDQJFZVtepTDdCjuBCe25Dw1Ils2qV4gPxn1VM_LCVzEl2__Zi3FLq15wY7j6FVZ0GZ6QBi8kFYwByyOZxSGX6pglliNZi336S4o4pjcEg5kZ0MNC7DeQwVgetMIi6UqJGfQeL8588vuaPMP00lXGt7oKLI0GsrBO67XG1g_O4Jzz.N43sP5tIG5FgdFM3IM9QMDgueQB6LbrdrVnD7KhIfXcgQJR5hA; _csrf=dVkg2axwnAHCGT4aHkcjJza9; connect.sid=s%3AT5HcEsD5mqe2018K0RWAkLibcHYRCMve.",
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
        print(title)
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
