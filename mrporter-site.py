#-*-encoding:utf8:-*-
''' --------------------------------- INPUT YOUR CONFIG --------------------------------- '''
MONITOR_DELAY = int(input(">>> Monitor Delay를 입력해주세요 (정수만) : ")) # second, if your input 10, monitor interval 10 second
discord_webhook = input(">>> 웹훅 URL을 입력해주세요 : ")
#MONITOR_DELAY = 5
#discord_webhook = 'https://discordapp.com/api/webhooks/481411222118465550/8TanFM9unt2Ztf_ySUGlus9MNw9DVDaTKNXAQZpMYvtnoucHevzCYn0gjwV_ZpQmKsTQ'
''' ------------------------------------------------------------------------------------- '''
import requests
from bs4 import BeautifulSoup
import time
import random
from log import *
from discord_hooks import Webhook

def send_embed(alert_type,product):
    '''
    (str, str, list, str, str, str) -> None
    Sends a discord alert based on info provided.
    '''
    # Set webhook
    url = discord_webhook

    # Create embed to send to webhook
    embed = Webhook(url, color=123123)

    # Set author info
    embed.set_author(name='Mrporter', icon='https://previews.123rf.com/images/martialred/martialred1604/martialred160400080/55731598-%EB%A9%94%EC%8B%9C%EC%A7%80-%EC%95%B1%EA%B3%BC-%EC%9B%B9-%EC%82%AC%EC%9D%B4%ED%8A%B8%EC%97%90-%EB%8C%80%ED%95%9C-chatbot-%EC%B1%84%ED%8C%85-%EB%B4%87-%EB%98%90%EB%8A%94-%EC%B1%84%ED%84%B0-%EB%B4%87-%EB%9D%BC%EC%9D%B8-%EC%95%84%ED%8A%B8-%EC%95%84%EC%9D%B4%EC%BD%98.jpg')

    # Set product details
    if(alert_type == "RESTOCK"):
        embed.set_desc("RESTOCK: " + "title")
    elif(alert_type == "NEW"):
        embed.set_desc("NEW: " + product.name)

    embed.add_field(name="Product", value=product.name)
    embed.add_field(name="Brand", value=product.brand)
    embed.add_field(name="Price", value=product.price)
    embed.add_field(name="Link", value=product.siteLik)
    embed.add_field(name="ImgLink", value=product.link)

    # Set product image
    #embed.set_thumbnail('https://cache.mrporter.com/images/products/1054353/1054353_mrp_fr_l.jpg')
    #embed.set_image(product.link)

    # Set footer
    embed.set_footer(text='Mrporter by @DevHong', icon='https://static.zerochan.net/Daenerys.Targaryen.full.2190849.jpg', ts=True)

    # Send Discord alert
    embed.post()
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
    :return: 현재 시간 time stamp를 반환
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
    # === 환경 설정 부분
    # 크롤링 해서 가져올 타켓팅 요소들의 CLASS NAME 이나, css, id 등의
    # attribute등을 정함
    SITE = 'https://www.mrporter.com/'
    BRAND_CLASS_NAME = 'pl-products-item__text pl-products-item__text--brand pl-products-item__text--upper'
    NAME_CLASS_NAME = 'pl-products-item__text pl-products-item__text--name'
    PRICE_CLASS_NAME = 'pl-products-item__text pl-products-item__text--price'
    IMG_CLASS_NAME = 'pl-products-item__img pl-products-item__spacing'

    # 페이지 넘버 기준으로 파싱을 하기위해서 pn = 뒤의 {}칸을 비운 포맷팅 변수
    URL_FORMAT = 'https://www.mrporter.com/en-jp/mens/shoes?pn={}'
    # =========

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


    # Page의 Total 수부분을 가져옴
    pageTotal = int(bs4.find('li', class_='pl-pagination__item pl-pagination__item--number').find_all('span')[
                        -1].get_text().strip())
    log('i',"Total {} Page exist".format(pageTotal))

    # 페이지의 마지막 까지 돌면서 DB를 구축한다.
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
            # 크롤링 부분 예를들면 brand는 span태그중 class이름이 위에 명시된 class_name
            # 인부분에 있다는 소리 이부분을 수정하면 다른 정보를 가져올수 있다.
            brand = li.find('span', class_=BRAND_CLASS_NAME).get_text().strip()
            name = li.find('span', class_=NAME_CLASS_NAME).get_text().strip()
            price = li.find('span', class_=PRICE_CLASS_NAME).get_text().strip()
            imgLink = li.find('div', class_=IMG_CLASS_NAME).img['src']
            siteLink = li.a['href']
            # 이미지링크가 //으로 되어있어 앞에 http 접두사와 //다음인 [2:] 슬라이싱 작업 실시
            products_list[siteLink] = Product(brand, name, price, 'https://' + imgLink[2:], SITE + siteLink)
    #

def monitor():
    # 빌딩_db 메서드와 맞춰주여야한다 .
    SITE = 'https://www.mrporter.com/'
    BRAND_CLASS_NAME = 'pl-products-item__text pl-products-item__text--brand pl-products-item__text--upper'
    NAME_CLASS_NAME = 'pl-products-item__text pl-products-item__text--name'
    PRICE_CLASS_NAME = 'pl-products-item__text pl-products-item__text--price'
    IMG_CLASS_NAME = 'pl-products-item__img pl-products-item__spacing'
    # seperate page url formatting var
    URL_FORMAT = 'https://www.mrporter.com/enjp/mens/shoes?pn={}'

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

    log('i', "Checking mrporter products...")
    bs4 = BeautifulSoup(r.text, "html.parser")
    lis = bs4.find_all('li', class_="pl-products-item")
    for li in lis:
        # 위와 동일
        brand = li.find('span', class_=BRAND_CLASS_NAME).get_text().strip()
        name = li.find('span', class_=NAME_CLASS_NAME).get_text().strip()
        price = li.find('span', class_=PRICE_CLASS_NAME).get_text().strip()
        imgLink = li.find('div', class_=IMG_CLASS_NAME).img['src']
        siteLink = li.a['href']
        try:
            #키의 존재유무를 보고
            products_list[siteLink]
        except:
            # 없어서 에러가 날경우는 새상품이 추가된 경우니
            # 알림 + DB에 insert를 한다 .
            log('s', "Added " + name + " to the database.")
            products_list[siteLink] = Product(brand, name, price, 'https://' + imgLink[2:], SITE + siteLink)
            send_embed('NEW',products_list[siteLink])



''' --------------------------------- RUN --------------------------------- '''
if __name__ == "__main__":
    # Ignore insecure messages
    # 웹훅때 이걸안하면 warning이 발생
    requests.packages.urllib3.disable_warnings()

    # 프록시를 읽어들인다.
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

    # Monitor products
    while (True):
        monitor()
        time.sleep(MONITOR_DELAY)



