import scrapy
from novel.items import Source, Novel, NovelChapter
from scrapy.http import HtmlResponse, FormRequest
from datetime import datetime
import re
import html
import json


class MetruyenfullIndexSpider(scrapy.Spider):
    name = "metruyenfull_index"
    allowed_domains = ["metruyenfull.org"]
    start_urls = ["https://metruyenfull.org/wp-admin/admin-ajax.php"]
    story_id = "453594"
    slug = "chang-re-manh-nhat-lich-su"
    title = "Chàng Rể Mạnh Nhất Lịch Sử"
    start_page = 1
    end_page = 20

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://metruyenfull.org",
        "Pragma": "no-cache",
        "Referer": "https://metruyenfull.org/chang-re-manh-nhat-lich-su",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
    }
    custom_settings = {"DEFAULT_REQUEST_HEADERS": headers, "ROBOTSTXT_OBEY": False}
    output_chapters = []

    def start_requests(self):
        for page in range(self.start_page, self.end_page + 1):
            form_data = {
                "action": "tw_ajax",
                "type": "pagination",
                "id": self.story_id,
                "page": str(page),
            }

            yield FormRequest(
                url=self.start_urls[0],
                formdata=form_data,
                headers=self.headers,
                callback=self.parse,
                meta={"page": page},  # Pass the page number to the parse method
            )

    def parse(self, response):
        data = response.json()

        htmlResponse = HtmlResponse(
            url="parse", body=data["list_chap"], encoding="utf-8"
        )

        # Source of novel ( page will be crawler )
        sourceItem = Source()
        sourceItem["id"] = "metruyenfull"
        sourceItem["name"] = "metruyenfull"
        sourceItem["domain"] = "https://metruyenfull.org"
        yield sourceItem

        # Novel Info
        novel = Novel()
        novel["source_id"] = "metruyenfull"
        novel["id"] = self.slug
        novel["name"] = self.name
        novel["slug"] = self.slug
        yield novel

        # Novel Episode
        listChapter = htmlResponse.css("ul.list-chapter > li > a")
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
            novelChapter["name"] = f"{novel_chapter_number} : {novel_chapter_title}"
            novelChapter["chapter_number"] = novel_chapter_number
            novelChapter["source_link"] = novel_link
            novelChapter["slug"] = novel_link.replace(
                f"https://metruyenfull.org/{self.slug}/", ""
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
