import scrapy
from novel.items import Source, Novel, NovelChapter
from scrapy.http import HtmlResponse
from datetime import datetime
import re
import html
import json


class DaoquanIndexSpider(scrapy.Spider):
    name = "daoquan_index"
    allowed_domains = ["daoquan.vn"]
    story_id = "371"
    start_urls = [
        f"https://api.daoquan.vn/web/c/storyChapters/sort?filter=%7B%22storiesId%22%3A{"371"}%7D&range=%5B{(page-75)}%2C{page}%5D"
        for page in range(75, 683, 75)
    ]
    slug = "chang-re-manh-nhat-lich-su"
    title = "Chàng Rể Mạnh Nhất Lịch Sử"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://daoquan.vn",
        "Pragma": "no-cache",
        "Referer": "https://daoquan.vn/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }
    custom_settings = {"DEFAULT_REQUEST_HEADERS": headers}
    total_page = 683
    output_chapters = []

    def parse(self, response):
        data = response.json()
        htmlResponse = body=data["result"]["list"]

        # Source of novel ( page will be crawler )
        sourceItem = Source()
        sourceItem["id"] = "daoquan"
        sourceItem["name"] = "daoquan"
        sourceItem["domain"] = "https://daoquan.vn"
        yield sourceItem

        # Novel Info
        novel = Novel()
        novel["source_id"] = "daoquan"
        novel["id"] = self.slug
        novel["name"] = self.name
        novel["slug"] = self.slug
        yield novel

        # Novel Episode
        listChapter = htmlResponse
        for chapter in listChapter:
            novel_link = f"https://daoquan.vn/dich-chang-re-manh-nhat-lich-su/{self.story_id}/1/chuong-{chapter["number"]}"
            novel_chapter_title = chapter["name"]
            novel_chapter_number = chapter["number"]

            novelChapter = NovelChapter()
            novelChapter["lang"] = "vi"
            novelChapter["novel_id"] = self.slug
            novelChapter["name"] = f"{novel_chapter_number} : {novel_chapter_title}"
            novelChapter["chapter_number"] = novel_chapter_number
            novelChapter["source_link"] = novel_link
            novelChapter["slug"] = novel_link.replace(
                f"https://daoquan.vn/dich-chang-re-manh-nhat-lich-su/", ""
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
