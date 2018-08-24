from discord_hooks import Webhook
webhook_url= input(">>> 웹훅 URL을 입력하세요:").strip()
def send_embed(alert_type,product):
    '''
    (str, str, list, str, str, str) -> None
    Sends a discord alert based on info provided.
    '''
    # Set webhook
    url = webhook_url
    #url = 'https://discordapp.com/api/webhooks/481411222118465550/8TanFM9unt2Ztf_ySUGlus9MNw9DVDaTKNXAQZpMYvtnoucHevzCYn0gjwV_ZpQmKsTQ'

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


send_embed('NEW',Product("테스트브랜드",'새로운신발이름','가격','https://www.mrporter.com//en-jp/mens/gucci/striped-rubber-slides/1054353','https://cache.mrporter.com/images/products/1054353/1054353_mrp_fr_m2.jpg'))