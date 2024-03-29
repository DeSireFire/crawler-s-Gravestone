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
from pprint import pprint

from fastapi import requests
import requests
# 统一响应的数据结构
from .models import Alamers, AlamerJobs
from server_core.control import constructResponse
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status, Query
from apps.projects.models import WorkerInfos, ProjectInfos, JobInfos
from .components import get_query_all, add_job_one, check_id_one, del_data_one, update_data

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
    if not check_id_one(AlamerJobs, name=data.get("name")):
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


@route.post("/update_alarmer_jobs", summary="修改告警任务")
async def update_alarmer_jobs(request: Request):
    fdata = await request.form()
    data = dict(fdata)
    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    name = data.get("name")
    aid = data.get("aid")
    a_jid = data.get("a_jid")
    data['delivery'] = int(data.get("delivery", 0))
    # 检测任务是否存在
    if check_id_one(Alamers, aid=aid):
        # 检测工作流是否存在
        if check_id_one(model=AlamerJobs, a_jid=a_jid):
            result = update_data(AlamerJobs, [data])
            if result:
                callbackJson.statusCode = 200
            else:
                callbackJson.resData["errMsg"] = "数据添加错误！"
        else:
            callbackJson.resData["errMsg"] = "告警任务不存在！无法修改状态"
    else:
        callbackJson.resData["errMsg"] = "所属的告警器！不存在！"
    return callbackJson.callBacker(content)




# 获取项目和工作流从属关系
@route.get("/get_pro_sub", summary="获取项目和工作流从属关系")
async def get_alarmer_jobs(request: Request):
    """
    获取项目和工作流从属关系
    const options = [
      {
        value: 'guide',
        label: 'Guide',
        children: [
          {
            value: 'disciplines',
            label: 'Disciplines',
          },
          {
            value: 'navigation',
            label: 'Navigation',
          },
        ],
      },
    ]
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    pro_res = get_query_all(ProjectInfos) or []
    work_res = get_query_all(WorkerInfos) or []
    res = []
    for p in pro_res:
        pid = p.get("pid")
        temp = {
            "label": p.get("name"),
            "value": p.get("pid"),
            "children": [],
        }
        for w in work_res:
            sub_temp = {
            "label": w.get("name"),
            "value": w.get("wid"),
            }
            if pid == w.get("pid"):
                temp["children"].append(sub_temp)
        res.append(temp)
    content = {}
    pprint(res)
    # 转换为业务响应数据
    content["list"] = res
    return callbackJson.callBacker(content)
