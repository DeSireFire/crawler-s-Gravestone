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
from fastapi.responses import JSONResponse

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

    def callBacker(self, data=None) -> object:
        if data is None:
            data = {}

        self.resData["statusCode"] = self.statusCode
        if 200 <= self.statusCode < 300:
            self.resData["statusBool"] = True
            self.message = "OK!"

        else:
            self.message = "响应处理时发生错误！" if not self.message else self.message
            self.resData["errCode"] = self.statusCode
            self.resData["errMsg"] = self.message
            self.resData["err_msg"] = self.message
            self.resData["statusBool"] = False
            logger.error(f"[{self.message}] url:{self.url}")

        if data:
            self.resData["data"] = data

        self.resData["message"] = self.message
        self.resData["ts"] = time.time()
        self.resData["date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # return self.resData

        return JSONResponse(status_code=self.statusCode, content=self.resData)