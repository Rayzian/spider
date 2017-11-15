# -*- coding: utf-8 -*-

import time
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')
headers = {
    'Host': 'client-api.itunes.apple.com',
    'User-Agent': 'iTunes/12.7.1 (Windows; Microsoft Windows 10 x64 Home Premium Edition (Build 14393); x64) AppleWebKit/7604.3005.2001.1',
    'Accept': '*/*',
    'Referer': 'https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?id=29099&popId=30&genreId=36',
    'Cookie': 'groupingPillToken=1_iphone#2_allPodcasts; xp_ab=1#isj11bm+461+17Eg4xa0; xp_abc=17Eg4xa0; xp_ci=3z1IUE28z8DWz4kkzCJvzpfOQGnKo',
    'Origin': 'https://itunes.apple.com',
    'Accept-Language': 'zh-cn',
    'X-Apple-I-MD-RINFO': '17106176',
    'X-Apple-Store-Front': '143465-19,32',
    'X-Apple-Tz': '28800',
    'X-Apple-I-MD': 'AAAABQAAABCz+zaogwbHFx/IOwdMSDnZAAAAAg==',
    'X-Apple-I-MD-M': 'YTA5cW0PwS8uWHwxAwTdeshI8vHzka6+lD6mZTAmiUlHKsEfKzUtZhGI8kzYBFq6KE5CyzI+l0sU7QOT',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Proxy-Connection': 'keep-alive'
}

def downloader(url, is_headers=True):
    s = requests.Session()
    web_data = None
    time.sleep(10)
    if is_headers:
        web_data = s.get(url=url, headers=headers)
    elif not is_headers:
        web_data = s.get(url=url)

    if web_data.status_code == 200:
        print "requests ", url, web_data.status_code
        time.sleep(5)
        return web_data.text
