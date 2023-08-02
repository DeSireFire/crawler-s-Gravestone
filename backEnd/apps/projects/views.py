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

from log_server.components import rename_log_file
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
    update_project_infos, get_query_all, add_data_one, check_id, get_fetch_one, del_data_one, update_data, add_job_one, \
    get_query_count, synchronous_workers, synchronous_jobs
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
    获取项目列表
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

@route.get("/get_projects_names", summary="获取所有项目名称")
async def get_projects_names(request: Request):
    """
    获取项目名称
    :param request:
    :param name:
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {}
    pro_list = get_projects_info() or []
    names = [v for k,v in pro_list.items() if k == "name"]
    # pprint(pro_list)
    # 转换为业务响应数据
    content["list"] = names or None
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
    workers_list = get_query_all(model=WorkerInfos, pid=pid) or []
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
    project_info = get_fetch_one(model=ProjectInfos, pid=pid)
    data["wid"] = temp_wid
    data["p_nickname"] = project_info.get("nickname")
    data["pid"] = pid
    # 检测所属项目存在
    if check_pid(pid=pid):
        # 检测工作流是否存在
        if not check_id(model=WorkerInfos, temp_id=temp_wid):
            result = add_data_one(WorkerInfos, data)
            if result:
                # 更新项目上面显示的工作流数量
                synchronous_workers(pid)
                callbackJson.statusCode = 200
            else:
                callbackJson.resData["errMsg"] = "数据添加错误！"
        else:
            callbackJson.resData["errMsg"] = "工作流已存在！"
    else:
        callbackJson.resData["errMsg"] = "未查询到所属项目！"
    return callbackJson.callBacker(content)


@route.delete("/del_workers", summary="删除工作流")
async def del_workers(request: Request, pid: str = Query(None), wid: str = Query(None)):
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

        # 更新项目上面显示的工作流数量
        synchronous_workers(pid)
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
    if pid:
        jobs_list = get_query_all(model=JobInfos, pid=pid) or []
    else:
        jobs_list = get_query_all(model=JobInfos) or []

    # pprint(jobs_list)
    # 转换为业务响应数据
    content["list"] = jobs_list or None
    content["pageTotal"] = len(jobs_list)
    return callbackJson.callBacker(content)


@route.delete("/del_jobs", summary="删除任务实例")
async def del_jobs(request: Request, pid: str = Query(None), wid: str = Query(None), jid: str = Query(None)):
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
        synchronous_jobs(del_data.get("pid"))
    else:
        callbackJson.statusCode = 404
        for k, v in jugements.items():
            if not v:
                callbackJson.message = k
    return callbackJson.callBacker(content)


@route.get("/get_log", summary="获取任务日志")
async def get_log(request: Request,
                  pid: str = Query(None),
                  wid: str = Query(None),
                  jid: str = Query(None),
                  lv:str = Query(None)
                  ):
    """
    获取任务日志
    :param request:
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {}
    print(f"pid:{pid}")
    job_info = get_query_all(model=JobInfos, pid=pid, wid=wid, jid=jid) or [{}]
    log_file_path = job_info[0].get("log_file_path", None)
    pprint(job_info)
    pprint(f"log_file_path --- > {log_file_path}")
    if lv:
        log_file_path = rename_log_file(log_file_path, lv)
    log_content = ""
    try:
        with open(log_file_path, encoding="utf-8") as f:
            log_content = f.read()
    except FileNotFoundError as FNFE:
        # 未找到指定文件
        log_content = "未查询到符合条件的日志..."

    # 转换为业务响应数据
    content["name"] = job_info[0].get("name", None)
    content["p_nickname"] = job_info[0].get("p_nickname", None)
    content["w_nickname"] = job_info[0].get("w_nickname", None)
    content["run_user"] = job_info[0].get("run_user", None)
    content["content"] = log_content or None
    return callbackJson.callBacker(content)


@route.post("/add_job", summary="新增任务")
async def add_job(request: Request, pid: str = Query(None), wid: str = Query(None), jid: str = Query(None)):
    """
    通过传入工作流实例wid等信息创建实际的任务实例记录

    wid: string;
    pid: string;
    p_nickname: string;
    name: string;
    nickname: string;
    crawl_frequency: string;
    description: string;
    status: string;
    modify_user: string;
    extra: string;
    create_time: string;
    update_time: string;

    :param request:
    :return:
    """
    fdata = await request.form()
    data = dict(fdata)
    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    result = add_job_one(JobInfos, data)
    # 同步项目下的任务数量
    synchronous_jobs(data.get("pid"))
    if result:
        jid = result.get_jid()
        callbackJson.statusCode = 200
        content["jid"] = jid
    return callbackJson.callBacker(content)


# todo 项目首页视图
@route.get("/get_ptasks", summary="获取任务状态饼图")
async def get_ptasks(request: Request, pid: str = Query(None)):
    """
    获取任务日志
    :param request:
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {}
    rjson = {
        "title": {
            "text": "数据统计 有点厉害",
        },
        "tooltip": {
            "trigger": "axis",
        },
        "legend": {
            "x": 'center',
            "y": 'bottom',
            "data": ["Email", "Union Ads", "Video Ads", "Direct", "Search Engine"],
        },
        "grid": {
            # "left": "3%",
            # "right": "4%",
            # "bottom": "3%",
            "containLabel": True,
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {},
            },
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {
            "type": "value",
        },
        "series": [
            {
                "name": "Email",
                "type": "line",
                "stack": "Total",
                "data": [120, 132, 101, 134, 90, 230, 210],
            },
            {
                "name": "Union Ads",
                "type": "line",
                "stack": "Total",
                "data": [220, 182, 191, 234, 290, 330, 310],
            },
            {
                "name": "Video Ads",
                "type": "line",
                "stack": "Total",
                "data": [150, 232, 201, 154, 190, 330, 410],
            },
            {
                "name": "Direct",
                "type": "line",
                "stack": "Total",
                "data": [320, 332, 301, 334, 390, 330, 320],
            },
            {
                "name": "Search Engine",
                "type": "line",
                "stack": "Total",
                "data": [820, 932, 901, 934, 1290, 1330, 1320],
            },
        ],
    }
    rjsons = []
    import random, copy
    # for i in range(1, random.randint(2, 5)):
    for i in range(1, 4):
        t = copy.deepcopy(rjson)
        t["title"]["text"] = f"数据统计({i})"
        for s in t["series"]:
            s["data"] = random_int_list(100, 999, 7)
        rjsons.append(t)
    content["list"] = rjsons
    # 转换为业务响应数据
    return callbackJson.callBacker(content)


def random_int_list(start, stop, length):
    import random
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list
