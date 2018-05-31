# -*- coding: utf-8 -*-

import time
import requests
import json
from DateOut import DataWrite

write = DataWrite()

headers = {
    'Host': 'api.maoyan.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'AiMovie /HUAWEI-8.0.0-MHA-AL00-1920x1080-440-8.3.7-8371-865970034074540-huawei'
}

url_list = [
    "http://api.maoyan.com/mmdb/movie/v3/list/hot.json?ci=59&limit=12&token=&utm_campaign=AmovieBmovieCD-1&movieBundleVersion=8371&utm_source=huawei&utm_medium=android&utm_term=8.3.7&utm_content=865970034074540&net=255&dModel=MHA-AL00&uuid=3C0A83B713E2C0868950C0EEB3F16C863B9D998126F29D93A6DF506E95527297&channelId=1&lat=30.581281&lng=104.047338&__reqTraceID=7007179182010740802&refer=c_wz7swafa&__skck=db33259ce537b3a9ac4d6f944c1ce1ad&__skts=1527594770088&__skua=d9fab342ebe50b7d4e484e2fe55dd709&__skno=5f2a4167-a51c-47b8-8e7a-d218ed907613&__skvs=1.1&__skcy=VZ0le10vnOn9Rcz4GBanKFzjg%2BM%3D HTTP/1.1",
    "http://api.maoyan.com/mmdb/movie/list/info.json?ci=59&headline=0&movieIds=343720%2C%20342791%2C%201196215%2C%201187542%2C%20341674%2C%20341178%2C%20879019%2C%20672164%2C%201217651%2C%201206839%2C%201210870%2C%201220095&token=&utm_campaign=AmovieBmovieCD-1&movieBundleVersion=8371&utm_source=huawei&utm_medium=android&utm_term=8.3.7&utm_content=865970034074540&net=255&dModel=MHA-AL00&uuid=3C0A83B713E2C0868950C0EEB3F16C863B9D998126F29D93A6DF506E95527297&channelId=1&lat=30.581485&lng=104.047611&__reqTraceID=-9145292217563416708&refer=c_wz7swafa&__skck=db33259ce537b3a9ac4d6f944c1ce1ad&__skts=1527598081273&__skua=d9fab342ebe50b7d4e484e2fe55dd709&__skno=ff4417c6-ab1d-4cdc-95ea-c1b917a7b263&__skvs=1.1&__skcy=hg99b%2BC52CmeQ%2FDeV3HeWm4Qmk4%3D HTTP/1.1",
    "http://api.maoyan.com/mmdb/movie/list/info.json?ci=59&headline=0&movieIds=1220905%2C%20603864%2C%20341941%2C%201199029%2C%20635863%2C%201218043%2C%201220853%2C%20342754%2C%201217637%2C%20881837%2C%20528054%2C%201218267&token=&utm_campaign=AmovieBmovieCD-1&movieBundleVersion=8371&utm_source=huawei&utm_medium=android&utm_term=8.3.7&utm_content=865970034074540&net=255&dModel=MHA-AL00&uuid=3C0A83B713E2C0868950C0EEB3F16C863B9D998126F29D93A6DF506E95527297&channelId=1&lat=30.581485&lng=104.047611&__reqTraceID=2692866237115754777&refer=c_wz7swafa&__skck=db33259ce537b3a9ac4d6f944c1ce1ad&__skts=1527598089823&__skua=d9fab342ebe50b7d4e484e2fe55dd709&__skno=640c5b30-ecd0-4768-b708-75ee9bda2667&__skvs=1.1&__skcy=lBcHDBkB6%2ByqgPzKsOjAvIkyq3Y%3D HTTP/1.1",
    "http://api.maoyan.com/mmdb/movie/list/info.json?ci=59&headline=0&movieIds=1215573%2C%2078187%2C%2078631%2C%20248551%2C%20346658%2C%20345972%2C%201203620%2C%201182552&token=&utm_campaign=AmovieBmovieCD-1&movieBundleVersion=8371&utm_source=huawei&utm_medium=android&utm_term=8.3.7&utm_content=865970034074540&net=255&dModel=MHA-AL00&uuid=3C0A83B713E2C0868950C0EEB3F16C863B9D998126F29D93A6DF506E95527297&channelId=1&lat=30.581485&lng=104.047611&__reqTraceID=3908726638037798479&refer=c_wz7swafa&__skck=db33259ce537b3a9ac4d6f944c1ce1ad&__skts=1527598091621&__skua=d9fab342ebe50b7d4e484e2fe55dd709&__skno=54645894-ef5e-461e-bbf9-a71bb25ccdd5&__skvs=1.1&__skcy=QNfpmSejGIFpVJqZoxAWDynaxMI%3D HTTP/1.1"

]

for url in url_list:

    s = requests.Session()
    web_data = s.get(url=url, headers=headers)

    if web_data.status_code == 200:
        print web_data.text
        web_data_json = json.loads(web_data.text)
        if web_data_json["data"]["hot"]:
            for info in web_data_json["data"]["hot"]:
                if not ("fra" in info):
                    local = u"中国"
                else:
                    local = info["fra"]

                data = {
                    "name": info["nm"],
                    "web": u"猫眼",
                    "movie_type": info["cat"],
                    "director": info["dir"],
                    "local": local,
                    "movieID": info["id"],
                    "actor": info["star"] if "star" in info else "null"
                }

                write.write(data=data)
                time.sleep(1)
        else:
            for info in web_data_json["data"]["movies"]:
                if "boxInfo" in info and unicode(info["boxInfo"]) == u"喵，即将上映":
                    continue

                if not ("fra" in info):
                    local = u"中国"
                else:
                    local = info["fra"]

                data = {
                    "name": info["nm"],
                    "web": u"猫眼",
                    "movie_type": info["cat"],
                    "director": info["dir"],
                    "local": local,
                    "movieID": info["id"],
                    "actor": info["star"] if "star" in info else "null"
                }

                write.write(data=data)
                time.sleep(1)

    time.sleep(10)
