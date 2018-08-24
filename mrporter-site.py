#-*-encoding:utf8:-*-
''' --------------------------------- INPUT YOUR CONFIG --------------------------------- '''
MONITOR_DELAY = 10 # second, if your input 10, monitor interval 10 second
discord_webhook = 'https://discordapp.com/api/webhooks/481411222118465550/8TanFM9unt2Ztf_ySUGlus9MNw9DVDaTKNXAQZpMYvtnoucHevzCYn0gjwV_ZpQmKsTQ'

''' ------------------------------------------------------------------------------------- '''
import requests
from bs4 import BeautifulSoup
import time
import random
from log import *

class Product:
    def __init__(self, brand, name, price, link, siteLik):
        self.link = link
        self.brand = brand
        self.name = name
        self.price = price
        self.siteLik = siteLik
def read_from_txt(path):
    '''
    (None) -> list of str
    Loads up all sites from the sitelist.txt file in the root directory.
    Returns the sites as a list
    '''
    # Initialize variables
    raw_lines = []
    lines = []

    # Load data from the txt file
    try:
        f = open(path, "r")
        raw_lines = f.readlines()
        f.close()

    # Raise an error if the file couldn't be found
    except:
        log('e', "Couldn't locate <" + path + ">.")

    if(len(raw_lines) == 0):
        pass
    # Parse the data
    for line in raw_lines:
        lines.append(line.strip("\n"))

    # Return the data
    return lines

def get_proxy(proxy_list):
    '''
    (list) -> dict
    Given a proxy list <proxy_list>, a proxy is selected and returned.
    '''
    # Choose a random proxy
    proxy = random.choice(proxy_list)

    # Set up the proxy to be used
    proxies = {
        "http": str(proxy),
        "https": str(proxy)
    }

    # Return the proxy
    return proxies

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

def build_db():
    # ===CONFIG
    # using variable webhook or crawling css, class, id attribute
    SITE = 'https://www.mrporter.com/'
    BRAND_CLASS_NAME = 'pl-products-item__text pl-products-item__text--brand pl-products-item__text--upper'
    NAME_CLASS_NAME = 'pl-products-item__text pl-products-item__text--name'
    PRICE_CLASS_NAME = 'pl-products-item__text pl-products-item__text--price'
    IMG_CLASS_NAME = 'pl-products-item__img pl-products-item__spacing'
    # seperate page url formatting var
    URL_FORMAT = 'https://www.mrporter.com/en-jp/mens/shoes?pn={}'
    # =========

    # GET "view all" page
    link = URL_FORMAT.format(1)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
    proxies = get_proxy(proxy_list)

    try:
        r = requests.get(link, timeout=5, verify=False)
    except:
        log('e', "Connection to URL <" + link + "> failed. Retrying...")
        try:
            if(use_proxies):
                proxies = get_proxy(proxy_list)
                r = requests.get(link, proxies=proxies, timeout=8, verify=False)
            else:
                r = requests.get(link, timeout=8, verify=False)
        except:
            log('e', "Connection to URL <" + link + "> failed.")
            return

    bs4 = BeautifulSoup(r.text, "lxml")

    #bs4 = get_bs_by_url(URL_FORMAT.format(1))
    # get page total cnt
    pageTotal = int(bs4.find('li', class_='pl-pagination__item pl-pagination__item--number').find_all('span')[
                        -1].get_text().strip())
    log('i',"Total {} Page exist".format(pageTotal))

    for pageNum in range(1, pageTotal + 1):
        log('i','{} page parsing...'.format(pageNum))
        # GET "view all" page
        link = URL_FORMAT.format(pageNum)
        try:
            r = requests.get(link, timeout=5, verify=False)
        except:
            log('e', "Connection to URL <" + link + "> failed. Retrying...")
            try:
                if (use_proxies):
                    proxies = get_proxy(proxy_list)
                    r = requests.get(link, proxies=proxies, timeout=8, verify=False)
                else:
                    r = requests.get(link, timeout=8, verify=False)
            except:
                log('e', "Connection to URL <" + link + "> failed.")
                return
        bs4 = BeautifulSoup(r.text, "lxml")
        lis = bs4.find_all('li', class_="pl-products-item")
        for li in lis:
            brand = li.find('span', class_=BRAND_CLASS_NAME).get_text().strip()
            name = li.find('span', class_=NAME_CLASS_NAME).get_text().strip()
            price = li.find('span', class_=PRICE_CLASS_NAME).get_text().strip()
            imgLink = li.find('div', class_=IMG_CLASS_NAME).img['src']
            siteLink = li.a['href']
            #print(DEBUG_PRINT.format(brand, name, price, imgLink, SITE + siteLink))
            products_list[siteLink] = Product(brand,name,price,imgLink,SITE + siteLink)
    #


''' --------------------------------- RUN --------------------------------- '''
if __name__ == "__main__":
    # Ignore insecure messages
    requests.packages.urllib3.disable_warnings()

    # Load proxies (if available)
    proxy_list = read_from_txt("proxies.txt")
    log('i', "Loaded " + str(len(proxy_list)) + " proxies.")
    if (len(proxy_list) == 0):
        use_proxies = False
    else:
        use_proxies = True

        # Initialize variables
    products_list = {}
    proxies = get_proxy(proxy_list)


    # Build database
    build_db()

    print(products_list)

    # Monitor products
    while (True):
        monitor()
        time.sleep(MONITOR_DELAY)

