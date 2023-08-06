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
from .models import Alamers, AlamerJobs
from server_core.control import constructResponse
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status, Query

from .components import get_query_all, add_job_one, check_id_one, del_data_one

route = APIRouter()


# 告警器视图
@route.get("/get_alarmers", summary="获取告警器列表")
async def get_alarmers(request: Request):
    """
    获取告警器表
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    res = get_query_all(Alamers) or []
    content = {}
    # 转换为业务响应数据
    content["list"] = res
    return callbackJson.callBacker(content)


@route.post("/add_alarmers", summary="创建告警器")
async def add_alarmers(request: Request):
    fdata = await request.form()
    data = dict(fdata)
    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    if not check_id_one(Alamers, name=data.get("name")):
        result = add_job_one(Alamers, data)
        if result:
            callbackJson.statusCode = 200
    return callbackJson.callBacker(content)


@route.delete("/del_alarmers", summary="删除告警器")
async def del_alarmers(request: Request):
    """
    接收要删除的数据，进行删除
    参数以url传参的方式接收，数据结构为
    :param request: 请求对象
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    del_data = dict(request.query_params)
    callbackJson.url = request.url
    content = del_data

    jugements = {
        "无效的文件..": True,
        "服务器找不到请求的资源": True,
    }

    if all(list(jugements.values())):
        res = del_data_one(model=Alamers, **del_data)
    else:
        callbackJson.statusCode = 404
        for k, v in jugements.items():
            if not v:
                callbackJson.message = k
    return callbackJson.callBacker(content)


# 告警任务视图
@route.get("/get_alarmer_jobs", summary="获取告警任务列表")
async def get_alarmer_jobs(request: Request):
    """
    获取告警任务列表
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    res = get_query_all(AlamerJobs) or []
    content = {}
    # 转换为业务响应数据
    content["list"] = res
    return callbackJson.callBacker(content)


@route.post("/add_alarmer_jobs", summary="添加告警任务")
async def add_alarmer_jobs(request: Request):
    """
    获取告警任务列表
    :return:
    """
    fdata = await request.form()
    data = dict(fdata)
    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    if not check_id_one(AlamerJobs, name=data.get("a_jid")):
        result = add_job_one(AlamerJobs, data)
        if result:
            callbackJson.statusCode = 200
    return callbackJson.callBacker(content)

@route.delete("/del_alarmer_jobs", summary="删除告警任务")
async def del_alarmer_jobs(request: Request):
    """
    接收要删除的数据，进行删除
    参数以url传参的方式接收，数据结构为
    :param request: 请求对象
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    del_data = dict(request.query_params)
    callbackJson.url = request.url
    content = del_data

    jugements = {
        "无效的文件..": True,
        "服务器找不到请求的资源": True,
    }

    if all(list(jugements.values())):
        res = del_data_one(model=AlamerJobs, **del_data)
    else:
        callbackJson.statusCode = 404
        for k, v in jugements.items():
            if not v:
                callbackJson.message = k
    return callbackJson.callBacker(content)


