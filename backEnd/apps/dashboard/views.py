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
    get_first_part_from_right, count_element_in_list, get_yesterday_finish_jobs, get_running_jobs_count, \
    get_total_jobinfos_count, count_logs_modified_yesterday, get_disk_space_percentage, get_items_count_by_wid, \
    summarize_logs_by_wid
from apps.users.models import get_user_count
from server_core.conf import BASE_DIR
from server_core.control import constructResponse

from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status, Query

route = APIRouter()


@route.get("/ipInfo")
async def ipInfo(request: Request):
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    # }
    #
    # response = requests.get('https://api.live.bilibili.com/xlive/web-room/v1/index/getIpInfo',
    #                         headers=headers)
    # temp = response.json()
    temp = {}
    client_ip = request.client.host
    print(f"client_ip: {client_ip}")
    return temp

# 日志统计
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

@route.get("/dboard_log_total")
async def dboard_log_proportion():
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    dboard_log_total = {}
    dboard_log_total['yesterday'] = summarize_logs_by_wid("yesterday")[:10]
    dboard_log_total['last_7_days'] = summarize_logs_by_wid("last_7_days")[:10]
    dboard_log_total['all_time'] = summarize_logs_by_wid("all_time")[:10]
    log_path = os.path.join(BASE_DIR, 'logs', 'worker_logs')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    dboard_log_total['proportion'] = get_folder_sizes(log_path)[:10]
    return callbackJson.callBacker(dboard_log_total)


@route.get("/dboard_info")
async def dboard_info():
    """
    仪表盘

    // 用户总数
    user_total: '--',
    // 程序总数
    programs_total: '--',
    // 日志总量
    logger_total: '--',
    // 项目总量
    project_total: '--',

    // 待定
    system_info: '--',
    // 内存占用
    memory_total: '--',
    // cpu占用
    master_cpu: '--',

    // 昨日任务完成
    yesterday_finish_jobs: '--',
    // 昨日任务数量
    yesterday_new_logger: '--',
    // 当前执行任务
    working_jobs: '--',
    // 任务总数
    jobs_total: '--',
    // 硬盘占用
    disk_total: '--',
    // 淘系接口应用调用
    taobao_captcha_api: '--'

    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    board_info = {}
    board_info["project_total"] = get_projects_count() or '--'
    board_info["user_total"] = get_user_count() or '--'
    board_info["system_info"] = '--'
    board_info["programs_total"] = get_programs_count() or '--'
    logs_path = os.path.join(BASE_DIR, "logs", "worker_logs") or '--'
    board_info["logger_total"] = list_files(logs_path)
    memory_total = get_memory_usage() or {}
    board_info["memory_total"] = memory_total.get("占用比例") or '--'
    board_info["master_cpu"] = get_machine_memory_usage_percent() or '--'

    board_info["yesterday_finish_jobs"] = get_yesterday_finish_jobs() or '--'
    directory_path = os.path.join(BASE_DIR, 'logs', 'worker_logs')
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    board_info["yesterday_new_logger"] = count_logs_modified_yesterday(directory_path) or '--'
    board_info["working_jobs"] = get_running_jobs_count() or '--'
    board_info["jobs_total"] = get_total_jobinfos_count() or '--'
    board_info["disk_total"] = get_disk_space_percentage() or '--'
    board_info["taobao_captcha_api"] = get_items_count_by_wid("daae2b53920ca33216bef79ccb27c651") or '--'
    pprint(board_info)
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