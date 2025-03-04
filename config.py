from database import *
import json


# 申购信息配置
applyNum = 3  # 申购次数
sleepTime = 5 # 每次申购间隔时间

# phone = ["18864928801","19534332008",]
# itemId = [['11318', '11319'],['11318', '11319']]
# userId = ["1104761773","1171733474"]
# token = [
#     "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJtdCIsImV4cCI6MTc0MjI3OTE2NywidXNlcklkIjoxMTA0NzYxNzczLCJkZXZpY2VJZCI6IjhENTZEOUVDLURCRDktREJEMC0yOUMzLURBNjQxQzJDRUIzNiIsImlhdCI6MTczOTY4NzE2N30.01NmUNyWuXaCu0RHPn6-xpG8tlm8p2YdxA8cOUO0niI",
#     "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJtdCIsImV4cCI6MTc0MjkwMDU3NSwidXNlcklkIjoxMTcxNzMzNDc0LCJkZXZpY2VJZCI6IjFDRDU4QTFDLUM1NjgtQjg1RS04QjhELTA4ODgyMzEwQzY3MiIsImlhdCI6MTc0MDMwODU3NX0.PDXNeCa3NKEX2reIc7G_Mo5wffXX1mwl5YyVOM5CHKI"
# ]
# cookie = [
#     "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJtdCIsImV4cCI6MTc0MjI3OTE2NywidXNlcklkIjoxMTA0NzYxNzczLCJkZXZpY2VJZCI6IjhENTZEOUVDLURCRDktREJEMC0yOUMzLURBNjQxQzJDRUIzNiIsImlhdCI6MTczOTY4NzE2N30.4trhpiFoECahMHzoulY1kCzxJhDqukv_ITksBR7bynk",
#     "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJtdCIsImV4cCI6MTc0MjkwMDU3NSwidXNlcklkIjoxMTcxNzMzNDc0LCJkZXZpY2VJZCI6IjFDRDU4QTFDLUM1NjgtQjg1RS04QjhELTA4ODgyMzEwQzY3MiIsImlhdCI6MTc0MDMwODU3NX0.kVss-KXyo6glVTYU-0-6t5gfEoQIaxnGmqwnMuWPJRg"
# ]


sqlData = get_db('config')
if len(sqlData) > 0:
    for i in sqlData:
        phone = i[1]
        itemId = json.loads(i[2])
        userId = i[3]
        cookie = i[4]
        token = i[5]
        for j in itemId:
            print(j,i)

