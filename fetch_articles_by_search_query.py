import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime 

keyword = input("Kata Kunci: ")
total_pages = input("Jumlah Artikel [10~100~1000]: ")
articles = []

for page in range(0, int(total_pages)):
    url = f"https://search.okezone.com/searchsphinx/loaddata/article/{keyword}/{page}"
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html5lib")

    article_scrape = soup.find("div", class_="listnews")

    published_time = article_scrape.find("div", class_="tgl").get_text()
    title = article_scrape.find("div", class_="title").get_text()
    href = article_scrape.a["href"]

    page_more = requests.get(href)
    soup_more = BeautifulSoup(page_more.text, "html5lib")

    content = ""
    paragraphs = soup_more.find("div", {"id": "contentx", "class": "read"}).find_all("p")
    for p in paragraphs:
        paragraph = p.get_text(strip=True)
        if not paragraph.endswith("*"):
            content += paragraph

    journalis = list(soup_more.find("div", class_="namerep").stripped_strings)[0].strip(",")
    
    articles.append({
        "published_time": published_time,
        "title": title,
        "content": content,
        "journalis": journalis,
        "url": href
    })

df = pd.DataFrame(articles)
# df.style.hide_index() | (this method has been DEPRECATED)
time_scrape = datetime.now().strftime("%m%d%Y_%H%M%S")
df.to_csv(f"result_by-query_{keyword}_{time_scrape}.csv", index=False)