from cores.core import core
from bs4 import BeautifulSoup
import os, requests, re

url = 'https://www.ptt.cc/bbs/Beauty/index.html'
main = core(url)
main.souphtml()
main.indexnum()
href = list()

##PTT外部目錄
def run(href,start=main.index ,pages=80, push=100):  
    ##start = input('想從哪開始: ')
    url = 'https://www.ptt.cc/bbs/Beauty/index'+ start +'.html'
    ##pages = input('爬幾頁: ')
    ##push = input('幾推以上: ')
    for i in range(pages):
        beauty = core(url)
        beauty.souphtml()
        beauty.titleinfo()
        beauty.pushnumber(beauty.items, push)
        ##beauty.titlename('自己')
        for item in beauty.items:
            href.append(item)
        beauty.nextpagehref()
        url = beauty.nextpage
        ##print(f'Go to {url}')

    for item in href:
        print(item)

#擷取文章內容，返回圖片網址
def content(href):
    r = requests.Session()
    r.post("https://www.ptt.cc/ask/over18?from=%2Fbbs%2FBeauty%2Findex.html", data = {'from':'/bbs/Beauty/index.html','yes':'yes'})
    r = r.get(href)
    soup = BeautifulSoup(r.text, 'lxml')
    soup = soup.find('div', {'id': 'main-content'})
    soup = soup.text.split('--')[0:-1]
    soup = ''.join(soup)
    soup = soup.split('\n')
    soup = soup[1:]
    for s in soup:    
        if '※ 發信站:' in s:
            soup = soup[:soup.index(s)]
    
    hrefRegex = re.compile(r'http(s)?://(i\.)?(m\.)?imgur\.com.*')
    hreflist = [href for href in soup if hrefRegex.search(href)]
    '''
    'http://i.imgur.com/A2wmlqW.jpg',
    'http://i.imgur.com/A2wmlqW',  # 沒有 .jpg
    'https://i.imgur.com/A2wmlqW.jpg',
    'http://imgur.com/A2wmlqW.jpg',
    'https://imgur.com/A2wmlqW.jpg',
    'https://imgur.com/A2wmlqW',
    'http://m.imgur.com/A2wmlqW.jpg',
    'https://m.imgur.com/A2wmlqW.jpg'
    '''
    return hreflist

# 轉換縮圖網址
def switch_href(href):
    if href.split('.')[-1] == 'jpg':
        name = href.split('/')
        truename = name[-1].split('.')[0]
        true_href = 'https://i.imgur.com/' + truename + '.jpg'
        print(true_href)  
        return true_href, truename + '.jpg'

    elif href.split('.')[-1] == 'gif':
        name = href.split('/')
        truename = name[-1].split('.')[0]
        true_href = 'https://i.imgur.com/' + truename + '.gif'
        print(true_href)  
        return true_href, truename + '.gif'
     
    elif href.split('.')[-1] == 'png':
        name = href.split('/')
        truename = name[-1].split('.')[0]
        true_href = 'https://i.imgur.com/' + truename + '.png'
        print(true_href)  
        return true_href, truename + '.png'

    else:
        print('此短網址沒有副檔名，暫時以gif替代')
        name = href.split('/')
        truename = name[-1]
        true_href = 'https://i.imgur.com/' + truename + '.gif'
        print(true_href)
        return true_href, truename + '.gif'

##擷取圖片網址，下載所有圖片
def img_download(hreflist, title_name):
    os.makedirs('./img/%s' % title_name,exist_ok=True)

    for href in hreflist:
        href, image_name = switch_href(href)
        r = requests.get(href, stream=True)
        try:
            print(f'開始下載{title_name}')
            with open('./img/%s/%s' % (title_name, image_name), 'wb') as f:
                for chunk in r.iter_content(chunk_size=128):
                    f.write(chunk)

        except Exception as e:
            print(f"{title_name} 無法下載，原因: ",e)

if __name__ == "__main__":
    start = input('想從哪一頁? ')
    pages = int(input("想爬幾頁? "))
    push = int(input('幾推? '))
    
    
    run(href, start=start, pages=pages, push=push)
    for item in href:
        hreflist = content(item[2])
        title_name = item[1]
        img_download(hreflist, title_name)