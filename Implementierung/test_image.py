import redis
import requests
from io import BytesIO
from PIL import Image
from config import Config

# connection to database
pool = Config.pool
redis = Config.redis

img_urls = ["https://bootdey.com/img/Content/avatar/avatar1.png",
            "https://bootdey.com/img/Content/avatar/avatar2.png",
            "https://bootdey.com/img/Content/avatar/avatar3.png",
            "https://bootdey.com/img/Content/avatar/avatar4.png",
            "https://bootdey.com/img/Content/avatar/avatar5.png"]

for index, img_url in enumerate(img_urls):
    output = BytesIO()
    im = Image.open(BytesIO(requests.get(img_url).content))
    im.save(output, format=im.format)

    redis.zadd("avatars", {output.getvalue(): index})
    output.close()
    redis.save  #redis-cli --raw get 'imgdata' >test.jpg


# get all avatars
avatars = redis.zrange("avatars", 0, -1)
for avatar in avatars:
    im = Image.open(BytesIO(avatar))
    im.show()
    im.close()