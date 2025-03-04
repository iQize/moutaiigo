import config
from function import *


# 获取公共参数
sessionId = str(get_session_id())  # 会话ID
shopAllInfo = get_all_shop_info()  # 所有店铺信息


for p in range(len(config.phone)):
    # 检查token是否失效
    data = get_user_info(config.phone[p], config.token[p], config.cookie[p])
    if data['code'] == 4011 or data['code'] == 4012:
        title = "Token已失效 - 茅台"
        desc = "登录账号："+config.phone[p]+"%0D%0A错误代码："+str(data['code'])+"%0D%0A请尽快前往NAS更新Token"
        requests.get("http://192.168.100.81:82/?title=" + title + "&description=" + desc + "&url=http://nas.eivo.top:5000")
        print("token失效")
    else:

        # 获取用户地址，默认第一个
        userAddInfo = get_user_info(config.phone[p], config.token[p], config.cookie[p])
        if userAddInfo['code'] == 2000:
            userAddLen = userAddInfo['data']['list']
            if len(userAddLen) > 0:
                userAddress = userAddLen[0]
                provinceName = userAddress['provinceName']
                lng = float(userAddress['longitude'])
                lat = float(userAddress['latitude'])

        # 获取店铺列表
        itemShopList = []

        for t in config.itemId[p]:
            shopList = get_shops(sessionId, provinceName, t)
            for i in shopList:
                shopsList = shopAllInfo[i['shopId']]
                shopLng = shopsList['lng']
                shopLat = shopsList['lat']
                shopInfo = {
                    "shopId": shopsList['shopId'],
                    "name": shopsList['name'],
                    "address": shopsList['fullAddress'],
                    "distance": get_distance(lat, lng, shopLat, shopLng),
                }
                itemShopList.append(shopInfo)
            
            # 排序
            itemShopList = sort_json_array(itemShopList, 'distance')

            jump = 0
            for j in itemShopList:
                data = apply(config.userId[p], j['shopId'], t, config.token[p], config.cookie[p], config.phone[p])
                if data['code'] == 2000:
                    title = "申购成功 - 茅台"
                    desc = "登录账号："+config.phone[p]+"%0D%0A店铺名称：" + j['name'] + "%0D%0A申购项目：" + t + "%0D%0A店铺地址：" + j['address'] + "%0D%0A距离：" + str(j['distance']) + "千米"
                    requests.get("http://192.168.100.81:82/?title=" + title + "&description=" + desc + "&url=http://nas.eivo.top:5000")
                    print(data)
                    time.sleep(config.sleepTime)
                    break
                else:
                    jump = jump + 1
                    if jump >= config.applyNum:
                        title = "申购失败 - 茅台"
                        desc = "登录账号："+config.phone[p]+"%0D%0A申购项目：" + t + "%0D%0A错误代码：" + str(data['code']) +  "%0D%0A错误信息：" + data['message'] +"%0D%0A点击前往NAS查看"
                        requests.get("http://192.168.100.81:82/?title=" + title + "&description=" + desc + "&url=http://nas.eivo.top:5000")
                        print(data)
                        time.sleep(config.sleepTime)
                        break
