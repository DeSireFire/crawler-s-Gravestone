#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/6/9
# CreatTIME : 14:12
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import random
import time
from server_core.log import logger
cache_datas = {}
if not cache_datas:
    pronames = [
        "高德地图",
        "美团药店",
        "企查查",
    ]
    datas = {"list": [], "pageTotal": 0}
    for i in range(0, random.randint(10, 100)):
        lines = {
            "id": random.randint(1, 100),
            "name": f"ip_{random.randint(1, 100)}_demo_local.log",
            "log_project": random.choice(pronames),
            "remarks": f"{random.randint(1, 12)}月-月度采集日志",
            "address": "localhost",
        }
        datas["list"].append(lines)
    datas["pageTotal"] = len(datas["list"])
    cache_datas = datas

class constructResponse(object):
    """
    统一响应构建器

    settings文件中的CUSTO_CALLBACK_DATA在这里也将会整合
    各apps的views响应的数据也会统一放置到BASE_CALLBACK_DATA的data字段里
    自动计算请求耗时，响应时间，时间戳，以及响应码和响应信息
    """
    def __init__(self):
        self.endTime = None
        self.resData = {}
        self.statusCode = 404
        self.message = None
        self.url = None

    def callBacker(self, data=None):
        if data is None:
            data = {}

        self.resData["statusCode"] = self.statusCode
        if 200 <= self.statusCode < 300:
            self.resData["statusBool"] = True
            self.message = "OK!"

        else:
            self.message = "数据拉取时发生错误！"
            logger.error(f"[数据拉取时发生错误] url:{self.url}")

        if data:
            self.endTime = time.time()
            self.resData["data"] = data

        self.resData["message"] = self.message
        self.resData["ts"] = self.endTime
        self.resData["date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return self.resData