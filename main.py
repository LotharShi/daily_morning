from datetime import datetime, timedelta
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now() + timedelta(hours=8)
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
anniversary = os.environ['START_DATE'][5:]

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
my_id = os.environ["MY_ID"]
template_id = os.environ["TEMPLATE_ID"]

weekday_dict = {1:u"一",2:u"二",3:u"三",4:u"四",5:u"五",6:u"六",7:u"天"}

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], str(math.floor(weather['low'])) + '~' + str(math.floor(weather['high'])) + '°C', weather['airData'], weather['airQuality']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_left(theday):
  next = datetime.strptime(str(today.year) + "-" + theday, "%Y-%m-%d")
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

def air_color(q):
    if q == '优':
        return '#228B22'
    elif q == '良':
        return '#DAA520'
    else :
        return '#B22222'

def get_today():
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    weekday = weekday_dict[today.weekday()+1]
    
    return year+'年'+month+'月'+day+'日'+' 星期'+weekday


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather, temperature, airData, airQuality = get_weather()
data = {"today":{"value":get_today(), "color":"#FFC0CB"}, "weather":{"value":weather, "color":"#808080"}, "temperature":{"value":temperature, "color":"#002FA7"}, "air":{"value":airData+' '+airQuality, "color":air_color(airQuality)}, "love_days":{"value":get_count(), "color": '#D70000'}, "birthday":{"value":get_left(birthday), "color":'#FF6347'}, "anniversary_left":{"value":get_left(anniversary), "color":'#FF69B4'}, "words":{"value":get_words(), "color":get_random_color()}}
res_user = wm.send_template(user_id, template_id, data)
res_my = wm.send_template(my_id, template_id, data)
print(res_user)
print(res_my)
print(today)
