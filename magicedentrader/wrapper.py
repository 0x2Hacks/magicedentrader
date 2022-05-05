from requests import Request, Session
import os
import requests
import time

_s = Session()

def _send(request):
    return _s.send(request.prepare()).json()

def get_collection_stats(symbol):
    url = "https://api-mainnet.magiceden.dev/v2/collections/{s}/stats".format(
        s = symbol
    )
    r = Request('GET', url)
    return _send(r)

def get_collection_listings(symbol, offset, limit=20):
    url = "https://api-mainnet.magiceden.dev/v2/collections/{s}/listings?offset={o}&limit={l}".format(
        s=symbol,
        o=offset,
        l=limit)
    r = Request('GET', url)
    return _send(r)

def get_collection_all_listings(symbol):
    test_request = get_collection_stats(symbol)
    pieces_num = test_request['listedCount']
    offset = 0
    pieces = []
    while offset < pieces_num:
        print(offset)
        pieces.extend(get_collection_listings(symbol, offset))
        offset += 20
        time.sleep(0.5)
    return pieces

def save_url(symbol, url, count):
    while True:
        try:
            img_data = requests.get(url).content
            with open(symbol+'/'+str(count)+'.jpg', 'wb') as handler:
                handler.write(img_data)
            break
        except Exception as e:
            print(e)

def get_collection_pics(symbol):
    listings = get_collection_all_listings(symbol)
    urls = [i['extra']['img'] for i in listings]
    if not os.path.exists(symbol):
        os.mkdir(symbol)
    count = 0
    for url in urls:
        save_url(symbol, url, count)
        count += 1