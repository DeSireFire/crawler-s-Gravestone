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
from .components import logrecord, file_log_save, traverse_folder, _handle_logfiles
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
    try:
        record = logrecord(data)
        # print(record)
        file_log_save(record)
        # demo_log_(record)
        # file_logger.log(
        #     int(record.levelno),
        #     record.getMessage()
        # )
        return {"status": "ok", "error": None, "data": data}
    except Exception as err:
        return {"status": "err", "error": err, "data": None}

@route.get("/get_logs")
async def get_logs(request: Request, name: str = Query(None)):
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


@route.get("/get_log_content")
async def get_log_content(request: Request, name: str = Query(None)):
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {
        "content": "",
    }
    log_info = dict(request.query_params)
    log_path = os.path.join(BASE_DIR, "logs", "worker_logs")
    print(f"log_path: {log_path}")
    print(f"log_info: {log_info}")

    filename = '1686885357069.log'

    # with open(os.path.join(log_path, filename), 'r') as f:
    #     content["content"] = f.read()

    for file in os.listdir(log_path):
        if os.path.isfile(os.path.join(log_path, file)) and file == filename:
            with open(os.path.join(log_path, file), 'r', encoding="utf-8") as f:
                content["content"] = f.read()

    return callbackJson.callBacker(content)