#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/30
# CreatTIME : 16:30
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import json
import logging
import os
# from .models import *
# from .auth import *
import time
from pprint import pprint

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status, Query
from fastapi.responses import JSONResponse
from .components import logrecord, file_log_save, traverse_folder, _handle_logfiles, is_file_locked
# 统一响应的数据结构
from server_core.control import constructResponse
from server_core.conf import BASE_DIR

from loguru import logger as sub_logger

route = APIRouter()


@route.post("/loguru")
async def update_loguru(request: Request):
    data = await request.body()
    fdata = await request.form()
    # 现在您可以使用 data 变量来访问请求发送来的数据
    log_data = data.decode("utf-8")
    # 日志转换 loguru
    log_record = dict(fdata)
    print(log_record)
    tmp = dict(fdata)
    message = log_record['msg']
    del tmp['levelname']
    del tmp['msg']
    sub_logger.bind(**tmp).log(log_record['levelname'], message)
    vs = [v for k, v in tmp.items()]
    print(" | ".join(vs))
    return {"data": data}


@route.post("/log")
async def update_logging(request: Request):
    data = await request.body()
    fdata = await request.form()
    print(f"{fdata}")
    try:
        record = logrecord(data)
        file_log_save(record)
        return {"status": "ok", "error": None, "data": data}
    except Exception as err:
        return {"status": "err", "error": err, "data": None}


@route.get("/get_logs", summary="获取指定日志列表")
async def get_logs(request: Request, name: str = Query(None)):
    """
    获取日志文件列表
    :param request:
    :param name:
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {}
    log_path = os.path.join(BASE_DIR, "logs", "worker_logs")
    # print(log_path)
    logs_files_dict = traverse_folder(log_path)
    pprint(logs_files_dict)

    # 转换为业务响应数据
    content.update(_handle_logfiles(logs_files_dict))

    return callbackJson.callBacker(content)


@route.get("/get_log_content", summary="获取指定日志内容")
async def get_log_content(request: Request, name: str = Query(None)):
    """
    获取日志文件内容
    :param request:
    :param name:
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {
        "content": "",
    }
    log_info = dict(request.query_params)
    logs_path = os.path.join(BASE_DIR, "logs", "worker_logs")
    filename = os.path.join(logs_path, log_info['log_project'], log_info['name'])

    with open(os.path.join(logs_path, filename), 'r', encoding="utf-8") as f:
        content["content"] = f.read()

    return callbackJson.callBacker(content)


@route.get("/get_log_project", summary="获取日志所属项目列表")
async def get_log_content(request: Request, name: str = Query(None)):
    """
    获取日志所属项目的列表
    :param request:
    :param name:
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {
        "log_projects": [],
    }
    log_info = dict(request.query_params)
    logs_path = os.path.join(BASE_DIR, "logs", "worker_logs")
    # 获取当前目录下的所有文件夹
    dirs = [d for d in os.listdir(logs_path) if os.path.isdir(d)]
    content["log_project"] = dirs
    return callbackJson.callBacker(content)


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
    del_data = dict(request.query_params)
    callbackJson.url = request.url
    content = del_data
    logs_path = os.path.join(BASE_DIR, "logs", "worker_logs")
    del_file_path = os.path.join(logs_path, del_data.get("log_project"), del_data.get("name"))

    jugements = {
        "无效的文件..": True if del_file_path else False,
        "服务器找不到请求的资源": os.path.exists(del_file_path),
        "该任务仍在执行中..暂不可删除": not is_file_locked(del_file_path),
    }

    if all(list(jugements.values())):
        os.remove(del_file_path)
    else:
        callbackJson.statusCode = 404
        for k, v in jugements.items():
            if not v:
                callbackJson.message = k
    return callbackJson.callBacker(content)
