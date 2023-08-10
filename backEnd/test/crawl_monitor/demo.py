#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/28
# CreatTIME : 11:09
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

"""
关于爬虫监控推送客户端的使用演示
"""


import requests
from logClient import CrawlLogUper

def crawl_demo():
    # 初始化推送器
    log_obj = CrawlLogUper(
        token="a158dc3a9d0f71283132f2c1127bc8c0",
        uper_name="tester",

        # ip_address="127.0.0.1",
        # port="50829",
        # 上传开关
        # up_switch=True
    )

    # 赋值内部方法，方便使用
    logger = log_obj.logger

    logger.info("这是一次采集动作的开始！")

    cookies = {
        'buvid3': '4EB0C268-F479-C4C0-BE14-9DE67C9C24AB10302infoc',
        'b_nut': '1667972110',
        'i-wanna-go-back': '-1',
        '_uuid': 'CA34F10C8-C3CD-641B-875B-5E55FE54F8D610922infoc',
        'LIVE_BUVID': 'AUTO8016693489848322',
        'buvid_fp_plain': 'undefined',
        'CURRENT_FNVAL': '4048',
        'rpdid': "|(um|JY~RlJ)0J'uY~|kmll~k",
        'nostalgia_conf': '-1',
        'buvid4': 'F8AED4AF-7298-F9DF-67C8-AC67BACE2D0D71690-022012514-PoU2UV%2F9Gkpp9Q6Q%2BxFUsQ%3D%3D',
        'theme_style': 'light',
        'CURRENT_PID': '2cabad50-e5a0-11ed-b4ec-3b5a3dd8f915',
        'DedeUserID': '201643',
        'DedeUserID__ckMd5': '9432afa3f7e7a0c1',
        'b_ut': '5',
        'home_feed_column': '4',
        'FEED_LIVE_VERSION': 'V8',
        'header_theme_version': 'CLOSE',
        'browser_resolution': '1280-625',
        'PVID': '1',
        'fingerprint': '71aa212908786512bb9715782905e123',
        'buvid_fp': '71aa212908786512bb9715782905e123',
        'hit-new-style-dyn': '0',
        'hit-dyn-v2': '1',
        'SESSDATA': '2a228f4e%2C1705716544%2Cc50d0%2A717jVDuAVbVPhZuALbpXVE1JpkfDf_TYHsRvgtof0AECg_-1OdbCqMRcgunis9sp91z2RO6QAAKwA',
        'bili_jct': '4519d750e423b3f27fef9f6b626eed47',
        'sid': '8skqbjcc',
        'bp_video_offset_201643': '822496545114947700',
        'innersign': '0',
        'b_lsid': '46C63CE10_18994FF3015',
    }

    headers = {
        'authority': 'api.live.bilibili.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7,und;q=0.6,ja;q=0.5',
        'cache-control': 'no-cache',
        # 'cookie': "buvid3=4EB0C268-F479-C4C0-BE14-9DE67C9C24AB10302infoc; b_nut=1667972110; i-wanna-go-back=-1; _uuid=CA34F10C8-C3CD-641B-875B-5E55FE54F8D610922infoc; LIVE_BUVID=AUTO8016693489848322; buvid_fp_plain=undefined; CURRENT_FNVAL=4048; rpdid=|(um|JY~RlJ)0J'uY~|kmll~k; nostalgia_conf=-1; buvid4=F8AED4AF-7298-F9DF-67C8-AC67BACE2D0D71690-022012514-PoU2UV%2F9Gkpp9Q6Q%2BxFUsQ%3D%3D; theme_style=light; CURRENT_PID=2cabad50-e5a0-11ed-b4ec-3b5a3dd8f915; DedeUserID=201643; DedeUserID__ckMd5=9432afa3f7e7a0c1; b_ut=5; home_feed_column=4; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; browser_resolution=1280-625; PVID=1; fingerprint=71aa212908786512bb9715782905e123; buvid_fp=71aa212908786512bb9715782905e123; hit-new-style-dyn=0; hit-dyn-v2=1; SESSDATA=2a228f4e%2C1705716544%2Cc50d0%2A717jVDuAVbVPhZuALbpXVE1JpkfDf_TYHsRvgtof0AECg_-1OdbCqMRcgunis9sp91z2RO6QAAKwA; bili_jct=4519d750e423b3f27fef9f6b626eed47; sid=8skqbjcc; bp_video_offset_201643=822496545114947700; innersign=0; b_lsid=46C63CE10_18994FF3015",
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    response = requests.get('https://api.live.bilibili.com/xlive/web-room/v1/index/getIpInfo', cookies=cookies,
                            headers=headers)
    temp = response.json() or {}

    logger.warning("假如，这里程序逻辑里，出现需要提示警告的情况，在这里打印警告日志")

    try:
        res = 1/0
    except Exception as e:
        logger.error(f'这是一条 错误 日志，错误信息6666：{e}')

    # 这里进行进行数据入库的逻辑
    temps = []
    if temp:
        temps.append(temp)
        print(temps)
        log_obj.items_total(len(temps))

    # 爬虫执行结束,调用完成方法。
    # log_obj.end_point()

if __name__ == '__main__':
    crawl_demo()
