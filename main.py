from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import time

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

user_id_2='o41cX6CjmkZRN-yyVwcs6TaaKB3s'
def getweek():
    """
    TODO:
    Wednesday 匹配数据出错，暂时无法解决
    :return:
    """
    try:
        week_en = time.strftime("%A", time.localtime(time.time()))
        week_list = {
            "Monday": "星期一",
            "Tuesday": "星期二",
            "Wednesday ": "星期三",
            "Thursday": "星期四",
            "Friday": "星期五",
            "Saturday": "星期六",
            "Sunday": "星期日"
        }
        currentTime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        week = week_list[week_en]
        day = currentTime + ' ' + week
        return day
    except Exception as e:
        currentTime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        day = currentTime + '  星期三'
        return day

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
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
wea, temperature = get_weather()
data = {"date": {"value": getweek(), "color": get_random_color()},"weather":{"value":wea, "color": get_random_color()},"temperature":{"value":temperature, "color": get_random_color()},"love_days":{"value":get_count(), "color": get_random_color()},"birthday_left":{"value":get_birthday(), "color": get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
res = wm.send_template(user_id_2, template_id, data)
