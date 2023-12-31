import requests
from config import USERS


def get_string_links(info):
    symbol = info['symbol']
    bid_price = info['bid_price']
    ask_price = info['ask_price']
    bid_qty = info['bid_qty']
    ask_qty = info['ask_qty']

    string = (
        f'Symbol: {symbol}\n'
        f'Bid price: {bid_price}\n'
        f'Ask price: {ask_price}\n'
        f'Bid price: {bid_qty}\n'
        f'Ask price: {ask_qty}\n'
    )
    return string

async def check_links():
    from main import bot

    url = "http://web:8000/api/v1/best-links-binance"
    response = requests.get(url)
    if response.status_code != 200:
        await bot.send_message(chat_id=USERS[0], text=str(response.status_code))
        return
    
    res = response.json()
    ads = res['data']
    
    allow_links = []

    for ad in ads:
        spread = ad['spread']
        if spread < 0.4: continue

        first = ad['first']
        second = ad['second']
        third = ad['third']
        spread = ad['spread']

        link = (
            f'Spread: {spread}%\n\n'
            f'{get_string_links(first)}\n'
            f'{get_string_links(second)}\n'
            f'{get_string_links(third)}\n'
        )
        allow_links.append(link)

    for user in USERS:
        for link in allow_links:
            await bot.send_message(chat_id=user, text=link)