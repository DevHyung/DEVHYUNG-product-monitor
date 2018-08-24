from discord_hooks import Webhook

def send_embed(alert_type):
    '''
    (str, str, list, str, str, str) -> None
    Sends a discord alert based on info provided.
    '''
    # Set webhook
    url = 'https://discordapp.com/api/webhooks/481411222118465550/8TanFM9unt2Ztf_ySUGlus9MNw9DVDaTKNXAQZpMYvtnoucHevzCYn0gjwV_ZpQmKsTQ'

    # Create embed to send to webhook
    embed = Webhook(url, color=123123)

    # Set author info
    embed.set_author(name='NERYS', icon='https://static.zerochan.net/Daenerys.Targaryen.full.2190849.jpg')

    # Set product details
    if(alert_type == "RESTOCK"):
        embed.set_desc("RESTOCK: " + "title")
    elif(alert_type == "NEW"):
        embed.set_desc("NEW: " + "title")

    embed.add_field(name="Product", value="title")
    embed.add_field(name="Link", value="link")
    embed.add_field(name="Stock", value="stock")

    # Set product image
    embed.set_thumbnail('https://static.zerochan.net/Daenerys.Targaryen.full.2190849.jpg')
    embed.set_image('https://static.zerochan.net/Daenerys.Targaryen.full.2190849.jpg')

    # Set footer
    embed.set_footer(text='NERYS by @snivynGOD', icon='https://static.zerochan.net/Daenerys.Targaryen.full.2190849.jpg', ts=True)

    # Send Discord alert
    embed.post()
send_embed('NEW')