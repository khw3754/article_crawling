from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def print_articles(entries, company, get_encoding):
    for entry in entries:
        title = entry["title"]
        link = entry["link"]
        try:
            date = entry["published"]
        except:
            date = "date없음"
        print(title)
        print(link)
        print(date)

        #### jtbc 본문 ####
        if company == "jtbc" :
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"class": "article_content"})

            print(content.getText().strip())

        #### 국민일보, 매일경제, 머니투데이, 헤럴드경제, 이데일리, mbn, 동아일보 본문 ####
        elif company in ["kukmin", "maeil", "moneytoday", "herald", "edaily", "mbn", "donga"] :
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            if company == "donga":
                # 본문만 남기고 좋아요 구독 같은 거 없애줌
                content.find(attrs={"class": "article_footer"}).decompose()

            print(content.getText().strip())

        #### 한국경제, 경향신문 본문 ####
        elif company == "hankyung" or company == "kyunghyang":
            # 헤더를 바꿔줘야 기사를 볼 수 있다.
            request_headers = {
                'User-Agent': ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
            Safari/537.36'), }

            article_res = requests.get(link, headers=request_headers)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            print(content.getText().strip())

        #### 조선일보 본문 ####
        elif company == "chosun":
            #조선일보의 [뉴스q]는 제외 (중복이다)
            if "뉴스Q" in title :
                continue

            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(link)
            element = WebDriverWait(driver, 3)\
                .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'section.article-body')))
            body = driver.find_element(By.CSS_SELECTOR, 'section.article-body')
            body = body.text
            print(body)

        #### sbs 본문 ####
        elif company == "sbs":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"class": "article_cont_area"})

            print(content.getText().strip())

        #### 한겨래 본문 ####
        elif company == "hankyoreh":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"class": "text"})

            print(content.getText().strip())

        #### 파이낸셜 본문 ####
        elif company == "financial":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"id": "article_content"})
            if content == None:
                content = soup.find("div", attrs={"itemprop": "articleBody"})

            try:
                print(content.getText().strip())
            except:
                print(title + "     본문 출력 오류남     " + link)


        print()

def save_articles(entries, company, get_encoding):
    file_path = "/Users/hyung/Desktop/article/" + company + "/"
    for entry in entries:
        title = entry["title"]
        link = entry["link"]

        try:
            f = open(file_path+title, 'w', encoding=get_encoding)
        except:
            print(file_path+title + "    file open 오류발생")
            continue

        #### jtbc 본문 ####
        if company == "jtbc":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"class": "article_content"})

            f.write(content.getText().strip())
            f.close()

        #### 국민일보 본문 ####
        elif company == "kukmin":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            f.write(content.getText().strip())
            f.close()

        #### 한국경제 본문 ####
        elif company == "hankyung":
            # 한국경제는 헤더를 바꿔줘야 기사를 볼 수 있다.
            request_headers = {
                'User-Agent': ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
                    Safari/537.36'), }

            article_res = requests.get(link, headers=request_headers)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            f.write(content.getText().strip())
            f.close()

        #### 매일경제 본문 ####
        elif company == "maeil":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            try:
                f.write(content.getText().strip())
                f.close()
            except:
                print(link)

        #### sbs 본문 ####
        elif company == "sbs":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"class": "article_cont_area"})

            f.write(content.getText().strip())
            f.close()

        #### 한겨래 본문 ####
        elif company == "hankyoreh":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"class": "text"})

            f.write(content.getText().strip())
            f.close()

        #### 경향신문 본문 ####
        elif company == "kyunghyang":
            request_headers = {
                'User-Agent': ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
                            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
                            Safari/537.36'), }

            article_res = requests.get(link, headers=request_headers)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            f.write(content.getText().strip())
            f.close()

        #### 동아일보 본문 ####
        elif company == "donga":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            # 본문만 남기고 좋아요 구독 같은 거 없애줌
            content.find(attrs={"class": "article_footer"}).decompose()
            f.write(content.getText().strip())
            f.close()

        #### 머니투데이 본문 ####
        elif company == "moneytoday":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            f.write(content.getText().strip())
            f.close()

        #### 해럴드경제 본문 ####
        elif company == "herald":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            f.write(content.getText().strip())
            f.close()

        #### 이데일리 본문 ####
        elif company == "edaily":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            f.write(content.getText().strip())
            f.close()

        #### 파이낸셜 본문 ####
        elif company == "financial":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"id": "article_content"})
            if content == None:
                content = soup.find("div", attrs={"itemprop": "articleBody"})

            try:
                f.write(content.getText().strip())
                f.close()
            except:
                print(title + "     본문 출력 오류남     " + link)

        #### mbn 본문 ####
        elif company == "mbn":
            article_res = requests.get(link)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            f.write(content.getText().strip())
            f.close()