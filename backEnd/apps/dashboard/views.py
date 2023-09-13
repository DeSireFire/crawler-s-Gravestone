#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/25
# CreatTIME : 17:29
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import math
import os
import random
from pprint import pprint

from fastapi import requests
import requests
# 统一响应的数据结构
from .components import list_files, get_machine_memory_usage_percent, \
    get_memory_usage, get_projects_count, get_programs_count, get_completed_jobs, get_folder_sizes, \
    get_first_part_from_right, count_element_in_list
from apps.users.models import get_user_count
from server_core.conf import BASE_DIR
from server_core.control import constructResponse

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


@route.get("/dboard_log_proportion")
async def dboard_log_proportion():
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    dboard_log_proportion = {}
    log_path = os.path.join(BASE_DIR, 'logs', 'worker_logs')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    dboard_log_proportion['list'] = get_folder_sizes(log_path)[:8]
    # print(dboard_log_proportion['list'])
    return callbackJson.callBacker(dboard_log_proportion)


@route.get("/dboard_info")
async def dboard_info():
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    board_info = {}
    # 用户数
    board_info["project_total"] = get_projects_count() or '--'
    board_info["user_total"] = get_user_count() or '--'
    board_info["system_info"] = '--'
    board_info["programs_total"] = get_programs_count() or '--'
    logs_path = os.path.join(BASE_DIR, "logs", "worker_logs") or '--'
    board_info["logger_total"] = list_files(logs_path)
    memory_total = get_memory_usage() or {}
    board_info["memory_total"] = memory_total.get("占用比例") or '--'
    board_info["master_cpu"] = get_machine_memory_usage_percent() or '--'

    return callbackJson.callBacker(board_info)

# 任务概览
@route.get("/dboard_jobs")
async def dboard_jobs():
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    dboard_jobs = {}
    # 获取符合筛选条件的数据
    temp_list = get_completed_jobs()

    # 将同工作流的任务数据筛出时间最新的一个
    has_work = []
    res_list = []
    for i in temp_list:
        name = i.get("name")
        work_name = get_first_part_from_right(name)
        if count_element_in_list(has_work, work_name) < 3:
            has_work.append(work_name)
            res_list.append(i)
    # pprint(temp_list)
    # print("*"*100)
    # pprint(res_list)
    dboard_jobs["list"] = res_list
    return callbackJson.callBacker(dboard_jobs)