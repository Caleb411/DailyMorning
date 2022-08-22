from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
gohome_date = os.environ['GOHOME_DATE']
my_city = os.environ['MY_CITY']
your_city = os.environ['YOUR_CITY']
my_birthday = os.environ['MY_BIRTHDAY']
your_birthday = os.environ['YOUR_BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather(city):
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['low']), math.floor(weather['high'])


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_gohome():
    delta = datetime.strptime(gohome_date, "%Y-%m-%d") - today
    return delta.days


def get_birthday_left(birthday):
    next = datetime.strptime(str(date.today().year) +
                             "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
my_weather, my_low, my_high = get_weather(my_city)
your_weather, your_low, your_high = get_weather(your_city)
data = {"my_weather": {"value": my_weather, "color": get_random_color()}, "my_low": {"value": my_low, "color": get_random_color()}, "my_high": {"value": my_high, "color": get_random_color()},
        "your_weather": {"value": your_weather, "color": get_random_color()}, "your_low": {"value": your_low, "color": get_random_color()}, "your_high": {"value": your_high, "color": get_random_color()},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "my_birthday_left": {"value": get_birthday_left(my_birthday), "color": get_random_color()},
        "your_birthday_left": {"value": get_birthday_left(your_birthday), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
