import pypub
import xml.etree.ElementTree as ET
import html
from bs4 import BeautifulSoup


def create_epub_from_xml(xml_filename, epub_filename):
    # Parse the XML file
    tree = ET.parse(xml_filename)
    root = tree.getroot()

    ebook = pypub.Epub("Mao sơn tróc quỷ nhân")

    # Iterate over each <item> in the XML file
    with open(f"{epub_filename}", "w", encoding="utf-8") as f:
        for item in root.findall("item"):
            title = item.find("title").text
            content = item.find("content").text
            soup = BeautifulSoup(content, "html.parser")

            for div_tag in soup.find_all("div"):
                div_tag.unwrap()

            chapter = pypub.create_chapter_from_text(
                soup.get_text(separator="\n", strip=True), title=title
            )
            ebook.add_chapter(chapter)

        ebook.create(f"./{epub_filename}")
    pass


# Example usage
create_epub_from_xml("mao-son-troc-quy-nhan.xml", "mao-son-troc-quy-nhan.epub")
