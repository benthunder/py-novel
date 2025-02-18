import scrapy
from novel.items import Source, Novel, NovelChapter
from scrapy.http import HtmlResponse
from datetime import datetime
import re
import html
import json


class InovelIndex6Spider(scrapy.Spider):
    name = "inovel6_index"
    allowed_domains = ["inovel6.com"]
    story_id = "6096e030594eec489c899620"
    start_urls = [
        f"https://inovel6.com/thong-tin-ca-nhan?story_id=6096e030594eec489c899620&page={page}"
        for page in range(1, 123)
    ]
    slug = "mao-son-troc-quy-nhan"
    title = "Mao Sơn Tróc Quỷ Nhân"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
    }
    custom_settings = {"DEFAULT_REQUEST_HEADERS": headers}
    total_page = 26
    output_chapters = []

    def parse(self, response):
        data = response.json()
        htmlResponse = HtmlResponse(
            url="parse", body=data["data"]["chaptersHtml"], encoding="utf-8"
        )

        # Source of novel ( page will be crawler )
        sourceItem = Source()
        sourceItem["id"] = "inovel6"
        sourceItem["name"] = "inovel6"
        sourceItem["domain"] = "https://inovel6.com"
        yield sourceItem

        # Novel Info
        novel = Novel()
        novel["source_id"] = "inovel6"
        novel["id"] = self.slug
        novel["name"] = self.name
        novel["slug"] = self.slug
        yield novel

        # Novel Episode
        listChapter = htmlResponse.css(".chapter-list a")
        for chapter in listChapter:
            novel_link = chapter.css("::attr(href)").get()
            novel_chapter_title = chapter.css("::attr(title)").get()
            novel_chapter_match = (
                re.search(r"chuong-(\d+)", novel_link) if novel_link else None
            )
            novel_chapter_number = (
                novel_chapter_match.group(1) if novel_chapter_match else None
            )

            novelChapter = NovelChapter()
            novelChapter["lang"] = "vi"
            novelChapter["novel_id"] = self.slug
            novelChapter["name"] = novel_chapter_title
            novelChapter["chapter_number"] = novel_chapter_number
            novelChapter["source_link"] = novel_link
            novelChapter["slug"] = novel_link.replace(
                f"https://inovel6.com/{self.slug}/", ""
            ).replace(".html", "")
            novelChapter["date_create"] = datetime.now().strftime("%d/%m/%Y")

            self.output_chapters.append(
                {
                    "chapter": novel_chapter_number,
                    "url": novel_link,
                    "title": html.unescape(novel_chapter_title),
                }
            )

            yield novelChapter
        pass

    def closed(self, reason):
        # Save to json
        with open(f"{self.slug}.json", "w", encoding="utf-8") as f:
            json.dump(self.output_chapters, f, ensure_ascii=False, indent=4)
