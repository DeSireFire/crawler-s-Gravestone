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
from .models import ProgramInfos
from server_core.conf import BASE_DIR
from server_core.control import constructResponse
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status, Query
from .components import get_query_all, add_data_one, check_id_one, del_data_one, update_data

route = APIRouter()


# 告警器视图
@route.get("/get_programs", summary="获取程序列表")
async def get_programs(request: Request):
    """
    获取程序列表
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    res = get_query_all(ProgramInfos) or []
    content = {}
    # 转换为业务响应数据
    content["list"] = res
    return callbackJson.callBacker(content)


@route.post("/add_program", summary="添加程序")
async def add_program(request: Request):
    fdata = await request.form()
    data = dict(fdata)
    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    if not check_id_one(ProgramInfos, name=data.get("name")):
        result = add_data_one(ProgramInfos, data)
        if result:
            callbackJson.statusCode = 200
    return callbackJson.callBacker(content)


@route.post("/update_program", summary="修改程序登记信息")
async def update_program(request: Request):
    fdata = await request.form()
    data = dict(fdata)
    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    cid = data.get("cid")
    # 检测任务是否存在
    if check_id_one(model=ProgramInfos, cid=cid):
        result = update_data(ProgramInfos, [data])
        if result:
            callbackJson.statusCode = 200
        else:
            callbackJson.resData["errMsg"] = "数据更新错误！"
    return callbackJson.callBacker(content)

@route.delete("/del_program", summary="删除程序")
async def del_program(request: Request):
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
        res = del_data_one(model=ProgramInfos, **del_data)
    else:
        callbackJson.statusCode = 404
        for k, v in jugements.items():
            if not v:
                callbackJson.message = k
    return callbackJson.callBacker(content)

@route.post("/deploy_program", summary="部署程序")
async def deploy_program(request: Request):
    """
    用于部署git上的项目
    :param request:
    :return:
    """
    fdata = await request.form()
    data = dict(fdata)
    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    git_repo = data.get("git_repo")

    # 查询是否登记在库
    if not check_id_one(ProgramInfos, cid=data.get("cid")):
        pass
        # result = add_data_one(ProgramInfos, data)
        # if result:
        #     callbackJson.statusCode = 200
    return callbackJson.callBacker(content)