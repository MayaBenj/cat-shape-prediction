import calendar
import time
from urllib.request import urlopen, Request

import requests
from PIL import Image

size = 224, 224

SUB_NAME = "CatsStandingUp"
SUB_NAME_UNDERSCORE = "cats_standing_up"

one_months = 2678400
before = calendar.timegm(time.gmtime())
after = before - one_months
TOP_POSTS = "https://api.pushshift.io/reddit/submission/search/?after=%s&before=%s&sort_type=score&sort=desc&subreddit=%s&size=500"

j = 0
i = 0
while True:
    for post in requests.get(TOP_POSTS % (str(after), str(before), SUB_NAME), headers={'User-agent': 'your bot 0.1'}).json()['data']:
        try:
            url = ""
            if post.get('media_metadata') is not None:
                url = post['media_metadata'][list(post['media_metadata'].keys())[0]]['s']['u']
            elif post.get('preview') is not None:
                url = post['url']
            if url:
                req = Request(url.replace("&amp;", "&"))
                req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36')
                # resize
                img = Image.open(urlopen(req)).resize(size)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                # save image
                img.save("{0}/{0}_{1}_{2}.jpg".format(SUB_NAME_UNDERSCORE, j, i))
                i += 1
        except Exception as e:
            print(e)
    print("Processed %d items" % i)
    print("Finished iteration %d" % j)
    j += 1
    before = after
    after -= one_months
