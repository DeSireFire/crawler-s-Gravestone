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
from fastapi import requests
import requests
# 统一响应的数据结构
from server_core.control import constructResponse,cache_datas

from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status, Query

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
    return callbackJson.callBacker(cache_datas)


@route.delete("/del_logs")  # todo 属于危险操作需要鉴权
async def del_logs(request: Request, name: str = Query(None)):
    """
    接收要删除的日志文件数据
    参数以url传参的方式接收，数据结构为
    {'id': '52', 'name': 'ip_89_demo_local.log', 'log_project': '美团药店', 'remarks': '12月-月度采集日志', 'address': 'localhost'}
    :param request: 请求对象
    :param name: 请求传输过来的name参数
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    callbackJson.url = request.url
    content = {}
    cache_list = cache_datas.get("list", [])
    del_data = dict(request.query_params)
    del_index = [i for i, x in enumerate(cache_list) if x == del_data]
    if del_index:
        content = cache_list.pop(del_index[0])
        cache_datas["list"] = cache_list
        cache_datas["pageTotal"] = len(cache_list)
    else:
        callbackJson.statusCode = 404
        callbackJson.message = "服务器找不到请求的资源"
    return callbackJson.callBacker(content)