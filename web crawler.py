import requests
from bs4 import BeautifulSoup
import os

# 定義headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# 設定爬取的推文數
push_threshold = 10

# 設定網址
url = 'https://www.ptt.cc/bbs/Beauty/index.html'

# 設定保存圖片的目錄
save_dir = 'ptt_beauty'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 設定cookies
cookies = {'over18': '1'}

# 建立會話
session = requests.session()
session.cookies.update(cookies)

while True:
    # 取得網頁內容
    response = session.get(url, headers=headers)

    # 解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 取得文章列表
    articles = soup.find_all('div', class_='r-ent')

    for article in articles:
        # 取得推文數
        push_count = article.find('div', class_='nrec').text.strip()
        if not push_count:
            push_count = 0
        elif push_count == '爆':
            push_count = 100
        elif push_count.startswith('X'):
            continue
        else:
            push_count = int(push_count)

        # 判斷推文數是否大於設定的閾值
        if push_count >= push_threshold:
            # 取得文章標題
            title = article.find('div', class_='title').text.strip()

            # 取得文章網址
            article_url = 'https://www.ptt.cc' + article.find('a')['href']

            # 取得文章內容
            response = session.get(article_url, headers=headers)
            article_soup = BeautifulSoup(response.text, 'html.parser')

            # 取得圖片連結
            image_links = article_soup.find_all('a', {'href': lambda s: s.endswith('.jpg') or s.endswith('.png')})

            # 下載圖片
            for link in image_links:
                image_url = link['href']
                save_path = os.path.join(save_dir, f'{title}_{image_url.split("/")[-1]}')
                with open(save_path, 'wb') as f:
                    response = session.get(image_url, headers=headers)
                    f.write(response.content)

    # 取得下一頁的網址
    next_link = soup.find('a', string='‹ 上頁')['href']
    url = 'https://www.ptt.cc' + next_link