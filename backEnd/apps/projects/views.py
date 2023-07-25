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
from datetime import datetime
from pprint import pprint
from typing import Dict

from fastapi.responses import JSONResponse
from server_core.control import constructResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status, Query
# 统一响应的数据结构
from server_core.conf import BASE_DIR
from loguru import logger as sub_logger

from utils.other import get_md5
from .components import \
    get_projects_info, check_pid, \
    add_project_info, del_project_info, \
    update_project_infos, get_query_all, add_data_one, check_id, get_fetch_one, del_data_one, update_data
from .models import WorkerInfos, ProjectInfos, JobInfos

route = APIRouter()

# 项目视图
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
async def update_project(request: Request):
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

@route.get("/get_project", summary="获取项目信息")
async def get_project(request: Request, pid: str = Query(None)):
    """
    更新项目信息
    :param request:
    :param pid:
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {}
    one = get_fetch_one(ProjectInfos, pid=pid) or []
    # pprint(pro_list)
    # 转换为业务响应数据
    content.update(one)
    return callbackJson.callBacker(content)

@route.get("/get_projects", summary="获取项目列表")
async def get_projects(request: Request):
    """
    更新项目列表
    :param request:
    :param name:
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {}
    pro_list = get_projects_info() or []
    # pprint(pro_list)
    # 转换为业务响应数据
    content["list"] = pro_list or None
    content["pageTotal"] = len(pro_list)
    return callbackJson.callBacker(content)

# 工作流视图
@route.get("/get_workers", summary="获取工作流列表")
async def get_workers(request: Request, pid: str = Query(None)):
    """
    获取工作流列表
    :param request:
    :param name:
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {}
    workers_list = get_query_all(model=WorkerInfos,pid=pid) or []
    pprint(workers_list)
    # 转换为业务响应数据
    content["list"] = workers_list or None
    content["pageTotal"] = len(workers_list)
    return callbackJson.callBacker(content)


@route.post("/add_workers", summary="新增工作流")
async def add_workers(request: Request):
    data = await request.body()
    fdata = await request.form()
    data = dict(fdata)

    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    name = data.get("name")
    pid = data.get("pid")
    temp_wid = get_md5(f"{name}_{pid}")
    pn = get_fetch_one(model=ProjectInfos, pid=pid).get("nickname")
    data["wid"] = temp_wid
    data["p_nickname"] = pn
    data["pid"] = pid
    # 检测所属项目存在
    if check_pid(pid=pid):
        # 检测工作流是否存在
        if not check_id(model=WorkerInfos, temp_id=temp_wid):
            result = add_data_one(WorkerInfos, data)
            if result:
                callbackJson.statusCode = 200
            else:
                callbackJson.resData["errMsg"] = "数据添加错误！"
        else:
            callbackJson.resData["errMsg"] = "工作流已存在！"
    else:
        callbackJson.resData["errMsg"] = "未查询到所属项目！"
    return callbackJson.callBacker(content)


@route.delete("/del_workers", summary="删除工作流")
async def del_project(request: Request, pid: str = Query(None), wid: str = Query(None)):
    """
    接收要删除的项目信息
    参数以url传参的方式接收，数据结构为
    :param request: 请求对象
    :param pid: 请求传输过来的pid参数
    :param wid: 请求传输过来的wid参数
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
        res = del_data_one(model=WorkerInfos, **del_data)
    else:
        callbackJson.statusCode = 404
        for k, v in jugements.items():
            if not v:
                callbackJson.message = k
    return callbackJson.callBacker(content)


@route.post("/update_workers", summary="修改工作流")
async def update_workers(request: Request):
    # data = await request.body()
    fdata = await request.form()
    data = dict(fdata)

    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    name = data.get("name")
    pid = data.get("pid")
    temp_wid = get_md5(f"{name}_{pid}")
    pn = get_fetch_one(model=ProjectInfos, pid=pid).get("nickname")
    data["p_nickname"] = pn
    # 检测所属项目存在
    if check_pid(pid=pid):
        # 检测工作流是否存在
        if not check_id(model=WorkerInfos, temp_id=temp_wid):
            result = update_data(WorkerInfos, [data])
            if result:
                callbackJson.statusCode = 200
            else:
                callbackJson.resData["errMsg"] = "数据添加错误！"
        else:
            callbackJson.resData["errMsg"] = "工作流已存在！"
    else:
        callbackJson.resData["errMsg"] = "未查询到所属项目！"
    return callbackJson.callBacker(content)


# 任务实例视图
@route.get("/get_jobs", summary="获取任务列表")
async def get_jobs(request: Request, pid: str = Query(None), wid: str = Query(None), jid: str = Query(None)):
    """
    获取任务列表
    :param request:
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {}
    print(f"pid:{pid}")
    jobs_list = get_query_all(model=JobInfos, pid=pid) or []
    # pprint(jobs_list)
    # 转换为业务响应数据
    content["list"] = jobs_list or None
    content["pageTotal"] = len(jobs_list)
    return callbackJson.callBacker(content)

@route.delete("/del_jobs", summary="删除任务实例")
async def del_project(request: Request, pid: str = Query(None), wid: str = Query(None), jid: str = Query(None)):
    """
    接收要删除的任务实例
    参数以url传参的方式接收
    :param request: 请求对象
    :param pid: 请求传输过来的pid参数
    :param wid: 请求传输过来的wid参数
    :param jid: 请求传输过来的jid参数
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
        res = del_data_one(model=JobInfos, **del_data)
    else:
        callbackJson.statusCode = 404
        for k, v in jugements.items():
            if not v:
                callbackJson.message = k
    return callbackJson.callBacker(content)