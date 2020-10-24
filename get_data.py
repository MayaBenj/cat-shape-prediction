from urllib.request import urlopen, Request

import requests
from PIL import Image

size = 128, 128

SUB_NAME = "CatsSittingDown"
SUB_NAME_UNDERSCORE = "cats_sitting_down"

TOP_POSTS = "https://www.reddit.com/r/%s/top/.json?t=%s&sort=top&after="

timeframes = ["month", "year", "all"]

for timeframe in timeframes:
    after = ""
    i = 0
    while i < 2000:
        for post in requests.get(TOP_POSTS % (SUB_NAME, timeframe) + after, headers={'User-agent': 'your bot 0.1'}).json()['data']['children']:
            try:
                url = ""
                if post['data'].get('media_metadata') is not None:
                    url = post['data']['media_metadata'][list(post['data']['media_metadata'].keys())[0]]['s']['u']
                elif post['data'].get('preview') is not None:
                    url = post['data']['url']
                if url:
                    req = Request(url.replace("&amp;", "&"))
                    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36')
                    # resize
                    img = Image.open(urlopen(req)).resize(size)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    # save image
                    img.save("{0}/{0}_{1}_{2}.jpg".format(SUB_NAME_UNDERSCORE, timeframe, i))
                    i += 1
            except Exception as e:
                print(e)
        print("Processed %d items" % i)
        # reached end of list
        if not requests.get(TOP_POSTS % (SUB_NAME, timeframe) + after, headers={'User-agent': 'your bot 0.1'}).json()['data']['children']:
            break
        # Get next page posts
        after = post['data']['name']

