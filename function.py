# i茅台函数
# 作者：迟善超
# 时间：2025.2.16
# 版本：1.0

# 公共依赖
import re
import requests
import json
import time
import math
import Encrypt
import datetime
from hashlib import md5
from bs4 import BeautifulSoup

# 盐值
Salf = "2af72f100c356273d46284f6fd1dfc08"

# AES加密值
AESKey = "qbhajinldepmucsonaaaccgypwuvcjaa"
AESIV = "2018534749963515"

# 加密解密
def crypto(data, type="encrypt"):
    aes = Encrypt.Encrypt(AESKey, AESIV)
    if type == "encrypt":
        return aes.aes_encrypt(data)
    return aes.aes_decrypt(data)

# 生成MD5
def hex_md5(str):
    m = md5()
    m.update(str.encode("utf-8"))
    return m.hexdigest()

# 获取设备ID
def get_device_id(phone):
    hash = hex_md5(phone)
    # 将 32 位的哈希值转换为 UUID 格式
    uuid_str = f"{hash[:8]}-{hash[8:12]}-{hash[12:16]}-{hash[16:20]}-{hash[20:]}"
    return uuid_str.upper()

# 获取时间戳
def get_time(len=13, t=None):
    if len == 13:
        if(t != None):
            dt = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
            return int(dt.timestamp() * 1000)
        return int(time.time() * 1000)
    if t != None:
        dt = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp())
    return int(time.time())

# 获取SessionId
def get_session_id():
    today_date = datetime.date.today().strftime("%Y-%m-%d 00:00:00")
    time = str(get_time(13,today_date))
    url = "https://static.moutai519.com.cn/mt-backend/xhr/front/mall/index/session/get/"+ time
    data = requests.get(url)
    if data.status_code != 200:
        return None
    return data.json()["data"]["sessionId"]

# 获取店铺列表
def get_shops(sessionId, province, itemId):
    today_date = datetime.date.today().strftime("%Y-%m-%d 00:00:00")
    time = str(get_time(13, today_date))
    url = "https://static.moutai519.com.cn/mt-backend/xhr/front/mall/shop/list/slim/v3/" + sessionId + "/" + province + "/"+ itemId +"/" + time
    data = requests.get(url)
    if data.status_code!= 200:
        return None
    return data.json()["data"]["shops"]

# 获取商品列表
def get_items(sessionId, province):
    today_date = datetime.date.today().strftime("%Y-%m-%d 00:00:00")
    time = str(get_time(13, today_date))
    url = "https://static.moutai519.com.cn/mt-backend/xhr/front/mall/shop/list/slim/v3/" + sessionId + "/" + province + "/10941/" + time
    data = requests.get(url)
    if data.status_code!= 200:
        return None
    return data.json()["data"]["items"]

# 获取店铺详情
def get_shop_info(shopId):
    url = "https://static.moutai519.com.cn/mt-backend/xhr/front/mall/resource/get"
    data = requests.get(url)
    if data.status_code!= 200:
        return None
    data_url = data.json()["data"]["mtshops_pc"]["url"]
    data = requests.get(data_url)
    if data.status_code != 200:
        return None
    return data.json()[shopId]

# 获取所有店铺详情
def get_all_shop_info():
    url = "https://static.moutai519.com.cn/mt-backend/xhr/front/mall/resource/get"
    data = requests.get(url)
    if data.status_code!= 200:
        return None
    data_url = data.json()["data"]["mtshops_pc"]["url"]
    data = requests.get(data_url)
    if data.status_code != 200:
        return None
    return data.json()

# 获取距离
def get_distance(lat1, lon1, lat2, lon2):
    #纬度 经度

    # 将角度转换为弧度
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine 公式
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # 地球半径，单位为千米
    earth_radius = 6371
    distance = earth_radius * c
    return round(distance, 2)

# 数组排序
def sort_json_array(array, name):
    array.sort(key=lambda x: x[name])
    return array

# 获取最新版本号
def get_mt_version():
    # apple商店 i茅台 url
    apple_imaotai_url = "https://apps.apple.com/cn/app/i%E8%8C%85%E5%8F%B0/id1600482450"
    response = requests.get(apple_imaotai_url)
    # 用网页自带的编码反解码，防止中文乱码
    response.encoding = "utf-8"
    html_text = response.text
    soup = BeautifulSoup(html_text, "html.parser")
    elements = soup.find_all(class_="whats-new__latest__version")
    # 获取p标签内的文本内容
    version_text = elements[0].text
    # 这里先把没有直接替换“版本 ”，因为后面不知道空格会不会在，所以先替换文字，再去掉前后空格
    latest_mt_version = version_text.replace("版本", "").strip()
    return latest_mt_version


# 获取用户地址信息
def get_user_info(phone, token, cookie):
    url = " https://h5.moutai519.com.cn/xhr/front/user/address/ship/query/v2?__timestamp=" + str(get_time(13))
    headre_data = {
        "device_id": str(get_device_id(phone)),
        "version": str(get_mt_version()),
        "token": token,
        "cookie": cookie
    }
    headres = request_header(headre_data)
    response = requests.get(url, headers=headres)
    return response.json()

# 请求头
def request_header(data=[]):
    return {
        "Content-Type": "application/json",
        "MT-Device-ID": str(data["device_id"]),
        "MT-Token": str(data["token"]),
        "MT-Info": "028e7f96f6369cafe1d105579c5b9377",
        "MT-Request-ID": "172086984219432249",
        "MT-APP-Version": str(data["version"]),
        "Cookie": "MT-Device-ID-Wap=" + str(data["device_id"]) + "; MT-Token-Wap=" + str(data["cookie"]),
        "BS-DVID": "jGhpB0y8ZIpW96q6Zpx1PcaTvHdRBBlZ62LzSdfPVJJ29n_wg0ZY_6be2CrCcR5c2ZfCGg2V1mTI9IdRkNqmwXQ",
        "MT-R": "clips_OlU6TmFRag5rCXwbNAQ/Tz1SKlN8THcecBp/HGhHdw==",
        "MT-User-Agent": "iOS;17.0.3;Apple;iPhone 13 Pro"
    }

# 发送验证码
def send_code(phone):
    url = "https://app.moutai519.com.cn/xhr/front/user/register/vcode"
    time = get_time(13)
    data = {
        "md5": hex_md5(Salf + phone + str(time)),
        "mobile": phone,
        "timestamp": str(time)
    }
    headre_data = {
        "device_id": str(get_device_id(phone)),
        "version": str(get_mt_version()),
        "token": "",
        "cookie": ""
    }
    headres = request_header(headre_data)
    response = requests.post(url, data=json.dumps(data), headers=headres)
    return response.json()

# 登录
def login(phone, code):
    url = "https://app.moutai519.com.cn/xhr/front/user/register/login"
    login_data = {
        "ydToken": "",
        "mobile": phone,
        "vCode": code,
        "ydLogId": ""
    }
    headre_data = {
        "device_id": str(get_device_id(phone)),
        "version": str(get_mt_version()),
        "token": "",
        "cookie": ""
    }
    headres = request_header(headre_data)
    response = requests.post(url, data=json.dumps(login_data), headers=headres)
    return response.json()


# 申购
def apply(userId, shopId, itemId, token, cookie, phone):
    url = "https://app.moutai519.com.cn/xhr/front/mall/reservation/add"
    itemInfoList = json.dumps({
        "itemInfoList":[{
            "count":1,
            "itemId":itemId
        }],
        "sessionId":get_session_id(),
        "userId":userId,
        "shopId":shopId
    })

    itemInfoList = re.sub(r"\s+", "", itemInfoList)
    actParam = crypto(itemInfoList, "encrypt")
    post_data = json.dumps({
        "actParam":actParam,
        "itemInfoList":[{
            "count":1,
            "itemId":itemId
        }],
        "shopId":shopId,
        "sessionId":get_session_id()
    })

    post_data = post_data.replace("/", "\\/")
    post_data = re.sub(r"\s+", "", post_data)

    headre_data = {
        "device_id": str(get_device_id(phone)),
        "version": str(get_mt_version()),
        "token": token,
        "cookie": cookie
    }

    headres = request_header(headre_data)
    data = requests.post(url, data=post_data, headers=headres)
    return data.json()

# 获取最近预约列表
def get_reserve(phone, token, cookie):
    url = "https://app.moutai519.com.cn/xhr/front/mall/reservation/list/pageOne/queryV2"
    headre_data = {
            "device_id": str(get_device_id(phone)),
            "version": str(get_mt_version()),
            "token": token,
            "cookie": cookie
        }
    headres = request_header(headre_data)
    data = requests.get(url, headers=headres)
    return data.json()

#{"code": 2000, "data": {"userId": 1104761773, "userName": "迟**", "mobile": "188****8801", "verifyStatus": 1, "idCode": "371581199605206054", "idType": 0, "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJtdCIsImV4cCI6MTc0MjI3OTE2NywidXNlcklkIjoxMTA0NzYxNzczLCJkZXZpY2VJZCI6IjhENTZEOUVDLURCRDktREJEMC0yOUMzLURBNjQxQzJDRUIzNiIsImlhdCI6MTczOTY4NzE2N30.01NmUNyWuXaCu0RHPn6-xpG8tlm8p2YdxA8cOUO0niI", "userTag": 0, "cookie": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJtdCIsImV4cCI6MTc0MjI3OTE2NywidXNlcklkIjoxMTA0NzYxNzczLCJkZXZpY2VJZCI6IjhENTZEOUVDLURCRDktREJEMC0yOUMzLURBNjQxQzJDRUIzNiIsImlhdCI6MTczOTY4NzE2N30.4trhpiFoECahMHzoulY1kCzxJhDqukv_ITksBR7bynk", "did": "did:mt:1:0x8fefaca6b44d250852b8fee0c595d30fa936d11bf6430e81fc070276a0c1b5c3", "birthday": "1996-05-20"}}
#"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJtdCIsImV4cCI6MTc0MjI3OTE2NywidXNlcklkIjoxMTA0NzYxNzczLCJkZXZpY2VJZCI6IjhENTZEOUVDLURCRDktREJEMC0yOUMzLURBNjQxQzJDRUIzNiIsImlhdCI6MTczOTY4NzE2N30.01NmUNyWuXaCu0RHPn6-xpG8tlm8p2YdxA8cOUO0niI
#"cookie": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJtdCIsImV4cCI6MTc0MjI3OTE2NywidXNlcklkIjoxMTA0NzYxNzczLCJkZXZpY2VJZCI6IjhENTZEOUVDLURCRDktREJEMC0yOUMzLURBNjQxQzJDRUIzNiIsImlhdCI6MTczOTY4NzE2N30.4trhpiFoECahMHzoulY1kCzxJhDqukv_ITksBR7bynk