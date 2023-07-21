#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/30
# CreatTIME : 16:30
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import os
import time
import json
import logging
from pprint import pprint
from typing import Dict

from fastapi.responses import JSONResponse
from server_core.control import constructResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status, Query
# 统一响应的数据结构
from server_core.conf import BASE_DIR
from loguru import logger as sub_logger
from .components import get_projects_info, check_pid, add_project_info, del_project_info,update_project_infos

route = APIRouter()

@route.post("/add_project", summary="创建项目")
async def add_project(request: Request):
    data = await request.body()
    fdata = await request.form()
    data = dict(fdata)

    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    if not check_pid(name=data.get("name")):
        result = add_project_info(data)
        if result:
            callbackJson.statusCode = 200
    return callbackJson.callBacker(content)

@route.post("/update_project", summary="修改项目")
async def add_project(request: Request):
    # data = await request.body()
    fdata = await request.form()
    data = dict(fdata)

    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    if check_pid(pid=data.get("pid")):
        result = update_project_infos(data)
        if result:
            callbackJson.statusCode = 200
    return callbackJson.callBacker(content)


@route.delete("/del_project", summary="删除项目")
async def del_project(request: Request, pid: str = Query(None)):
    """
    接收要删除的项目信息
    参数以url传参的方式接收，数据结构为
    :param request: 请求对象
    :param name: 请求传输过来的name参数
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
        # os.remove(del_file_path)
        res = del_project_info(del_data)
    else:
        callbackJson.statusCode = 404
        for k, v in jugements.items():
            if not v:
                callbackJson.message = k
    return callbackJson.callBacker(content)


@route.get("/get_projects", summary="获取项目列表")
async def get_projects(request: Request):
    """
    新项目
    :param request:
    :param name:
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {}
    pro_list = get_projects_info()
    pprint(pro_list)
    # 转换为业务响应数据
    content["list"] = pro_list
    content["pageTotal"] = len(pro_list)
    return callbackJson.callBacker(content)
