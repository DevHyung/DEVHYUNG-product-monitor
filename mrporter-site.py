import requests
from bs4 import BeautifulSoup

def get_bs_by_url(_url):
    """
    :param _url: target URL
    :return: bs4 object
    """
    return BeautifulSoup(requests.get(_url).text,'lxml')
if __name__ == "__main__":
    #===CONFIG
    # using variable webhook or crawling css, class, id attribute
    SITE = 'https://www.mrporter.com/en-jp/'
    BRAND_CLASS_NAME = 'pl-products-item__text pl-products-item__text--brand pl-products-item__text--upper'
    NAME_CLASS_NAME = 'pl-products-item__text pl-products-item__text--name'
    PRICE_CLASS_NAME = 'pl-products-item__text pl-products-item__text--price'
    IMG_CLASS_NAME ='pl-products-item__img pl-products-item__spacing'

    URL_FORMAT ='https://www.mrporter.com/en-jp/mens/shoes?pn={}'

    debug_print = """
    브랜드 :{}
    이름  :{}
    가격  :{}
    이미지 :{}
    """
    #=========
    bs4 = get_bs_by_url(URL_FORMAT.format(1))
    lis = bs4.find_all('li',class_="pl-products-item")
    for li in lis[:5]:
        brand = li.find('span',class_=BRAND_CLASS_NAME).get_text().strip()
        name = li.find('span',class_=NAME_CLASS_NAME).get_text().strip()
        price = li.find('span',class_=PRICE_CLASS_NAME).get_text().strip()
        imgLink = li.find('div',class_=IMG_CLASS_NAME).img['src']
        print(debug_print.format(brand,name,price,imgLink))