from cores.core import core
from bs4 import BeautifulSoup
import os, requests, re

url = 'https://www.ptt.cc/bbs/Gamesale/index.html'
main = core(url)
main.souphtml()
main.indexnum()
href = list()

##PTT外部目錄
def run(href, buysold, titlename, start=main.index ,pages=20, push=100):  
    ##start = input('想從哪開始: ')
    url = 'https://www.ptt.cc/bbs/Gamesale/index'+ start +'.html'
    ##pages = input('爬幾頁: ')
    ##push = input('幾推以上: ')
    for i in range(pages):
        gamesale = core(url)
        gamesale.souphtml()
        gamesale.titleinfo()
        gamesale.titlename(buysold)
        gamesale.titlename(titlename)
        for item in gamesale.items:
            href.append(item)
        gamesale.nextpagehref()
        url = gamesale.nextpage
        print(f'Go to {url}')

    '''for item in href:
        print(item)'''
        
#擷取文章內容
def content(href):
    r = requests.Session()
    r.post("https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGamesale%2Findex.html", data = {'from':'/bbs/Gamesale/index.html','yes':'yes'})
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
    
    return '\n'.join(soup)

##抓出當頁的資訊（遊戲名, 價錢, 網址）
def information(url):
    PriceResult = []
    ProductResult = []
    
    soup = content(url)
    

    productRegex = re.compile(r'★.*物.*品.*名.*稱.*?★|【\s{,100}物.*品.*名.*稱.*?【', re.DOTALL)
    productresult = productRegex.search(soup)
    
    if productresult != None:
        productresult = productresult.group().split('\n')
        productresult = [x for x in productresult if (x != '' and x != '★' and x != '【' and x != '★【')]
        
        for product in productresult:
            product = product.strip()          
            ProductResult.append(product)
     

    priceRegex = re.compile(r'★【\s{,100}售.*價.*?★|★【\s{,100}?徵.*求.*價.*?★|【\s{,100}售.*價.*?【|【\s{,100}?徵.*求.*價.*?【',re.DOTALL)
    priceresult = priceRegex.search(soup)

    if priceresult != None or priceresult != list():
        priceresult = priceresult.group().split('\n')
        priceresult = [x for x in priceresult if (x != '' and x != '★' and x != '【' and x != '★【')]
        
        for price in priceresult:
            price = price.strip()
            PriceResult.append(price)
    


    '''for product in productresult:
        if (name in product) or (productresult.index(product) == 0):
            index = productresult.index(product)
            ProductResult.append(productresult[index])
            PriceResult.append(priceresult[index])'''
    return '\t'.join(ProductResult), '\t'.join(PriceResult), url

if __name__ == "__main__":
    buysold = input('徵? 售? ')
    titlename = input('標題關鍵字? ') 
    pages= int(input('爬幾頁? '))
    
    run(href, buysold, titlename, start=main.index, pages=pages)
    for item in href:
        product, price, url = information((item[2]))
        print(product)
        print(price)
        print('【網    址】：',url)
        print('\n')