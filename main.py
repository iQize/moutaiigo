import config
from function import *


# 获取公共参数
sessionId = str(get_session_id())  # 会话ID
shopAllInfo = get_all_shop_info()  # 所有店铺信息


for p in range(len(config.phone)):
    # 检查token是否失效
    data = get_user_info(config.phone[p], config.token[p], config.cookie[p])
    if data['code'] == 4011 or data['code'] == 4012:
        print("token失效")
        break
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
                    print(data)
                    time.sleep(config.sleepTime)
                    break
                else:
                    jump = jump + 1
                    if jump >= config.applyNum:
                        print(data)
                        time.sleep(config.sleepTime)
                        break
