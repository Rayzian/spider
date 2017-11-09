# -*- coding: utf-8 -*-

import time
import threading
from AppSpiders.pcsuite360.newGameParse import Paser

def start_work(url, type, plat):
    p = Paser()
    p.json_parse(url=url, type=type, plat=plat)



if __name__ == '__main__':
    # url1 = "http://openbox.mobilem.360.cn/app/rank?from=game&type=new&prepage=game_ranking&curpage=game_ranking_%E6%96%B0%E6%A6%9C_%E5%85%A8%E9%83%A8&page=1&os=19&os_version=4.4.4&vc=300070109&v=7.1.9&md=MuMu&sn=6.119186756728438&cpu=&ca1=x86&ca2=armeabi-v7a&m=94a9af57156152abdd51228b0a31c7a6&m2=a6b2959a7e642787f4d28fd04dc2b942&ch=110149&ppi=720_1280&startCount=1&pvc=82&pvn=1.0.82&re=1&tid=0&cpc=1&snt=-1&nt=1&gender=-1&age=0&theme=2&br=Android&s_3pk=1"

    url2 = "http://openbox.mobilem.360.cn/app/rank?from=game&type=good_sale&prepage=game_ranking&curpage=game_ranking_%E7%83%AD%E6%A6%9C_%E5%85%A8%E9%83%A8&page=1&os=19&os_version=4.4.4&vc=300070109&v=7.1.9&md=MuMu&sn=6.119186756728438&cpu=&ca1=x86&ca2=armeabi-v7a&m=94a9af57156152abdd51228b0a31c7a6&m2=a6b2959a7e642787f4d28fd04dc2b942&ch=110149&ppi=720_1280&startCount=1&pvc=82&pvn=1.0.82&re=1&tid=0&cpc=1&snt=-1&nt=1&gender=-1&age=0&theme=2&br=Android&s_3pk=1"

    # th1 = threading.Thread(target=start_work, args=(url1, "new_games", "360PCSuite", ), name="Th1")
    th2 = threading.Thread(target=start_work, args=(url2, "good_sales", "360PCSuite", ), name="Th2")

    # th1.start()
    # time.sleep(1)
    th2.start()

    # th1.join()
    th2.join()