import cloudscraper

scraper = cloudscraper.create_scraper()  # Automatically handles Cloudflare's anti-bot page
url = "https://novelbin.com/ajax/chapter-archive?novelId=absolute-sword-sense"

response = scraper.get(url)
print(response.text)
