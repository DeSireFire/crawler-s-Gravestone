#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/25
# CreatTIME : 17:29
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import math
import random

import requests
# 统一响应的数据结构
from server_core.control import constructResponse,cache_datas
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status

route = APIRouter()
@route.get("/ipInfo")
async def ipInfo():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    response = requests.get('https://api.live.bilibili.com/xlive/web-room/v1/index/getIpInfo',
                            headers=headers)
    temp = response.json()
    return temp



@route.get("/get_logs")
async def get_logs():
    callbackJson = constructResponse()
    callbackJson.statusCode = 200

    # todo 翻页逻辑如何传递

    return callbackJson.callBacker(cache_datas)
