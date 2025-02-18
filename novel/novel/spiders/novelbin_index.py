import scrapy
from novel.items import Source, Novel, NovelChapter
from scrapy.http import HtmlResponse
from datetime import datetime
import re
import html
import json


class NovelBinIndexSpider(scrapy.Spider):
    name = "novelbin_index"
    allowed_domains = ["novelbin.com"]
    # story_id = "371"
    slug = "absolute-sword-sense"
    start_urls = [f"https://novelbin.com/ajax/chapter-archive?novelId={slug}"]

    title = "Tuyệt đối kiếm cảm"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version": '"133.0.3065.59"',
        "sec-ch-ua-full-version-list": '"Not(A:Brand";v="99.0.0.0", "Microsoft Edge";v="133.0.3065.59", "Chromium";v="133.0.6943.60"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"10.0.0"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "cookie": "_ga=GA1.1.1029526527.1739389877; _sharedID=bc09a410-2dc0-45bb-be3e-2214b08d2a7a; _sharedID_cst=kSylLAssaw%3D%3D; _ym_uid=1739389878838924839; _ym_uid_cst=kSylLAssaw%3D%3D; _lr_env_src_ats=false; _DABPlus6355_userid_consent_data=6683316680106290; _csrf=zUPzvNLj_6Ktfp7rOqJXeGDH; connect.sid=s%3AHALuhVzL5bUI2BX22Gv4Jhua0p5Ggctj.SN1A59HjMAV%2F1Tt2%2B%2B0gmHXaNFLpNbax42B7cg5NUyc; _gaClientId=1029526527.1739389877; _lr_retry_request=true; pbjs-id5id=%7B%22signature%22%3A%22ID5_Ah1YUhbhmLlctlalc0SKWZ7z21xsuLBo75TfsB3dtALHbvzGj5lF0d-VmbRX7NQK2vZT0D5n2mR3QXqUJcdfjMqkIkTspg8DRYLRj1uHuhq17rcYA4rEFe4c5cyJlrMfZbgkhONBMIF2gYVT2dmraV6w6PYj3OsdulpH3LhmHH_mgpkmKvY%22%2C%22created_at%22%3A%222024-12-06T05%3A53%3A15.974Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*cxXe55EqIxzmnFMFHHPl7KBRatUtHdewQ89JnVBsdoT4mQEDYo29aIwHgqoCtFlQ%22%2C%22universal_uid%22%3A%22ID5*H_xRIKmw9qFtmtKFFUG160LQXuny6XkxoVGLdTIcuUv4mchYOngACY_5d8J_bon_%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%2C%22ext%22%3A%7B%22linkType%22%3A2%2C%22pba%22%3A%22QYHsUy112rYGCu9SNmQfRfCGH2xw4TrkRv2umcNwxr0%3D%22%7D%2C%22cache_control%22%3A%7B%22max_age_sec%22%3A7200%7D%2C%22ids%22%3A%7B%22id5id%22%3A%7B%22eid%22%3A%7B%22source%22%3A%22id5-sync.com%22%2C%22uids%22%3A%5B%7B%22id%22%3A%22ID5*H_xRIKmw9qFtmtKFFUG160LQXuny6XkxoVGLdTIcuUv4mchYOngACY_5d8J_bon_%22%2C%22atype%22%3A1%2C%22ext%22%3A%7B%22linkType%22%3A2%2C%22pba%22%3A%22QYHsUy112rYGCu9SNmQfRfCGH2xw4TrkRv2umcNwxr0%3D%22%7D%7D%5D%7D%7D%7D%7D; pbjs-id5id_cst=zix7LPQsHA%3D%3D; pbjs-id5id_last=Thu%2C%2013%20Feb%202025%2007%3A14%3A57%20GMT; _ga_15YCML7VSC=GS1.1.1739430836.2.1.1739431148.0.0.0; cf_clearance=DreOyPdcFbJhXbzoPbNSGRjQP2UjIyh99Jjb58xmzeY-1739432013-1.2.1.1-9CO0qsl03N9m2.Ghjyfvb4AIdfykHFIlWugMxEJSmmavD_csHG16O3Qs7wN0AUQIsQrnxRqrk3YjV66ES8ImskTNsWqnDmaqf0gyPWeusqd1bEEudr9AYemgsq.vuqqpN_e3cyCLshVJc67K4yyla4MretwMQT1WD_M5t959tYTmB0agQ3f3ALFg_kShZDYoeY6gB3_xQJon2mZm4Ru4i6OKI.sWCp3_myP2UkDST5m.6xH25v7bjpTSXn5Iu.dzHs3JpGdtoWtfDt8SQVXRQkyuq0YEPMolQz_cN_hlZ.tSB1QWLo_WtAK8FpL_xyNKaaMLE79vug13I0YPDKrxNg",
    }

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": headers,
        "COOKIES_ENABLED": True,
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_splash.SplashCookiesMiddleware": 723,
            "scrapy_splash.SplashMiddleware": 725,
            "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
        },
        "HTTPERROR_ALLOWED_CODES": [403],
    }
    total_page = 683
    output_chapters = []

    def parse(self, response):
        print(response.text())
        exit()
        data = response.json()
        htmlResponse = body = data["result"]["list"]

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
