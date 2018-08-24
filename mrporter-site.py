#-*-encoding:utf8:-*-

''' --------------------------------- INPUT YOUR CONFIG --------------------------------- '''

MONITOR_DELAY = 10 # second, if your input 10, monitor interval 10 second
PAGE_MOVE_DELAY = 1 # second, if your input 1, page move interval 1 second
''' ------------------------------------------------------------------------------------- '''
import requests
from bs4 import BeautifulSoup
import time
def get_now_time():
    """
    :return: now time stamp
    """
    now = time.localtime()
    return "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
def get_bs_by_url(_url):
    """
    :param _url: target URL
    :return: bs4 object
    """
    return BeautifulSoup(requests.get(_url,timeout=5).text,'lxml')
''' --------------------------------- RUN --------------------------------- '''
if __name__ == "__main__":
    #===CONFIG
    # using variable webhook or crawling css, class, id attribute
    SITE = 'https://www.mrporter.com/'
    BRAND_CLASS_NAME = 'pl-products-item__text pl-products-item__text--brand pl-products-item__text--upper'
    NAME_CLASS_NAME = 'pl-products-item__text pl-products-item__text--name'
    PRICE_CLASS_NAME = 'pl-products-item__text pl-products-item__text--price'
    IMG_CLASS_NAME ='pl-products-item__img pl-products-item__spacing'
    # seperate page url formatting var
    URL_FORMAT ='https://www.mrporter.com/en-jp/mens/shoes?pn={}'
    # for DEVBUG
    DEBUG_PRINT = """
    브랜드 :{}
    이름  :{}
    가격  :{}
    이미지 :{}
    링크  :{}
    """
    #=========
    #===MONITOR
    oldProductList = [] # Privious prod list

    bs4 = get_bs_by_url(URL_FORMAT.format(1))
    # get page total cnt
    pageTotal = int ( bs4.find('li',class_='pl-pagination__item pl-pagination__item--number').find_all('span')[-1].get_text().strip() )
    print(">>> Total {} Page exist".format(pageTotal))

    for pageNum in range(1,pageTotal+1):
        bs4 = get_bs_by_url(URL_FORMAT.format(pageNum))
        lis = bs4.find_all('li',class_="pl-products-item")
        for li in lis[:1]:
            brand = li.find('span',class_=BRAND_CLASS_NAME).get_text().strip()
            name = li.find('span',class_=NAME_CLASS_NAME).get_text().strip()
            price = li.find('span',class_=PRICE_CLASS_NAME).get_text().strip()
            imgLink = li.find('div',class_=IMG_CLASS_NAME).img['src']
            siteLink = li.a['href']
            print(DEBUG_PRINT.format(brand,name,price,imgLink,SITE+siteLink))
        time.sleep(PAGE_MOVE_DELAY)