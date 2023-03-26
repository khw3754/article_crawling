import feedparser
from bs4 import BeautifulSoup
import requests

from rssCrawl import print_articles
from rssCrawl import save_articles

# companies = {"https://fs.jtbc.co.kr/RSS/newsflash.xml": "jtbc", "https://fs.jtbc.co.kr/RSS/politics.xml": "jtbc",
#              "https://fs.jtbc.co.kr/RSS/economy.xml": "jtbc", "https://fs.jtbc.co.kr/RSS/society.xml": "jtbc",
#              "https://fs.jtbc.co.kr/RSS/international.xml": "jtbc", "https://fs.jtbc.co.kr/RSS/culture.xml": "jtbc",
#              "https://fs.jtbc.co.kr/RSS/entertainment.xml": "jtbc", "https://fs.jtbc.co.kr/RSS/sports.xml" : "jtbc",
#              "http://rss.kmib.co.kr/data/kmibRssAll.xml": "kukmin",
#              "https://rss.hankyung.com/feed/economy.xml": "hankyung", "https://rss.hankyung.com/feed/it.xml": "hankyung",
#              "https://rss.hankyung.com/feed/international.xml": "hankyung", "https://rss.hankyung.com/feed/life.xml": "hankyung",
#              "https://rss.hankyung.com/feed/sports.xml": "hankyung", "https://rss.hankyung.com/feed/stock.xml": "hankyung",
#              "https://rss.hankyung.com/feed/land.xml": "hankyung", "https://rss.hankyung.com/feed/politics.xml": "hankyung",
#              "https://rss.hankyung.com/feed/society.xml": "hankyung", "https://rss.hankyung.com/feed/hei.xml": "hankyung",
#              "https://www.mk.co.kr/rss/40300001/": "maeil"}
# companies = {"https://www.mk.co.kr/rss/40300001/": "maeil"}
for url, company in companies.items() :
    #먼저 받아옴
    res = requests.get(url)
    html = res.text

    #인코딩 방식 추출
    dd = html.index("encoding=")
    get_encoding = html[dd + 10:dd + 16]
    res.encoding = get_encoding             #인코딩 방식 지정 -- 안하면 깨지는 제목들 있음
    html = res.text

    d = feedparser.parse(html)

    entries = d.entries
    entry_count = len(entries)

    # print(entries)
    print(entry_count, company, get_encoding)
    print("-----------------------------------------------------------")

    ###### 출력 테스트 ######
    print_articles(entries, company, get_encoding)


    ###### 저장 테스트 #####
    # save_articles(entries, company, get_encoding)