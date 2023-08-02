#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/26
# CreatTIME : 18:04
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import asyncio
import json
import os

import uvicorn
from pprint import pprint
from fastapi import FastAPI

from apps.projects import get_fetch_one, JobInfos, update_data, WorkerInfos, constructResponse, add_job_one, \
    synchronous_jobs
from server_core.conf import redisconf
from utils.RedisDBHelper import RedisDBHelper
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, APIRouter, Body, Depends, status, Query
from log_server.components import create_log_message, count_logs_by_level, log_to_save
from server_core.conf import BASE_DIR

app = FastAPI()
rdb = RedisDBHelper(redisconf.db if redisconf.db else 0)
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/log2", summary="日志传输接口")
async def log(data: str):
    rdb.set('log', data)
    return {"status": "success"}

@app.post("/log")
async def update_logging(request: Request):
    """
    接收客户端日志
    {'args': '()',
     'created': '1690426537.0822754',
     'exc_info': 'None',
     'exc_text': 'None',
     'extra': '{"ip": "192.168.9.193", "log_name": "单例爬虫测试日志", "project_name": '
              '"高德地图", "token": "a158dc3a9d0f71283132f2c1127bc8c0"}',
     'filename': 'logClient.py',
     'funcName': '<module>',
     'levelname': 'DEBUG',
     'levelno': '10',
     'lineno': '112',
     'module': 'logClient',
     'msecs': '82.275390625',
     'msg': '这是一条 调试 日志，发出来测试一下！！！ cpu占用：57%',
     'name': '单例爬虫测试日志',
     'pathname': 'F:\\workSpace\\myGithub\\crawler-s-Gravestone\\backEnd\\log_server\\logClient.py',
     'process': '15080',
     'processName': 'MainProcess',
     'relativeCreated': '146.44455909729004',
     'stack_info': 'None',
     'thread': '1028',
     'threadName': 'MainThread'}
    {'ip': '192.168.9.193',
     'log_name': '单例爬虫测试日志',
     'project_name': '高德地图',
     'token': 'a158dc3a9d0f71283132f2c1127bc8c0'}

    :param request:
    :return:
    """
    data = await request.body()
    fdata = await request.form()
    # 获取日志流传送的信息
    log_data = fdata.__dict__.get('_dict')

    # 日志附加信息
    extra_data = json.loads(log_data.get("extra"))
    # 日志等级
    log_level = log_data['levelname']
    # 工作流密钥
    token = extra_data.get('token', 'unknown')
    wid = extra_data.get("token")
    jid = extra_data.get("jid")
    status = extra_data.get("status") or 0
    items_count = extra_data.get("items_count") or 0
    try:
        # 同步到数据库
        # 获取工作流信息=>
        # 生成任务实例的jid=>
        # 通过jid获取任务实例信息，如果没有就生成新的任务实例=>

        # 调用函数并打印结果
        log_details = create_log_message(log_data)
        redis_log_key = f"crawl_monitor:logging:{jid}"
        sub_redis_log_key = f"crawl_monitor:logging:{jid}:{log_level}"
        rdb.lpush(redis_log_key, log_details.get("log_record"))
        rdb.lpush(sub_redis_log_key, log_details.get("log_record"))

        # 使用 Redis 的INCR命令对计数器进行原子递增
        lv_total = count_logs_by_level([log_data])

        # 同步监控数据到数据库
        job_info = get_fetch_one(JobInfos, jid=jid)

        # 状态
        # 0 未知，1 执行中，2 结束， 3 中断， 4 失败
        if status:
            job_info["status"] = status
        else:
            job_info["status"] = job_info["status"] if job_info["status"] else 3

        # 入库数据计数
        if job_info["items_count"] == None:
            job_info["items_count"] = 0
        if items_count:
            job_info["items_count"] += items_count or 0

        job_info["log_lv_info"] = lv_total.get(jid, {}).get('INFO') or job_info["log_lv_info"]
        job_info["log_lv_error"] = lv_total.get(jid, {}).get('ERROR') or job_info["log_lv_error"]
        job_info["log_lv_warning"] = lv_total.get(jid, {}).get('WARNING') or job_info["log_lv_warning"]
        del job_info["create_time"]
        del job_info["end_time"]
        job_info_new = update_data(JobInfos, [job_info])

        # 获取日志文件路径
        log_file_path = job_info.get("log_file_path")
        log_to_save(redis_log_key, log_file_path, log_level)
        # asyncio.run(log_to_save2(redis_log_key, log_file_path))

        # 状态的控制，销毁前发送状态，推送时修改状态，atexit 模块的尝试
        # todo 演示爬虫项目
        # todo 演示的文本
        # todo 谷歌历史记录

        return {"status": "ok", "error": None, "data": data}
    except Exception as err:
        return {"status": "err", "error": err, "data": None}

@app.post("/add_job", summary="新增任务")
async def add_job(request: Request, pid: str = Query(None), wid: str = Query(None), jid: str = Query(None)):
    """
    通过传入工作流实例wid等信息创建实际的任务实例记录
    :param request:
    :return:
    """
    data = await request.body()
    fdata = await request.form()
    data = dict(fdata)

    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}

    wid = data.get("wid", None)
    init_mark = data.get("init_mark", None)


    # 没有wid传入，直接返回失败
    if not wid:
        return callbackJson.callBacker(content)

    # wid 获取工作流信息
    winfo = get_fetch_one(WorkerInfos, wid=data.get("wid"))
    # 没获取到直接返回失败
    # todo 返回时说明错误原因
    if not winfo:
        return callbackJson.callBacker(content)

    project_name = winfo.get('name')

    log_file_name = f"{winfo.get('name')}-{init_mark}"
    log_file_path = os.path.join(BASE_DIR, "logs", "worker_logs", project_name, f"{log_file_name}.log")
    data["log_file_path"] = log_file_path
    del data['init_mark']
    result = add_job_one(JobInfos, data)
    worker = get_fetch_one(WorkerInfos, wid=data.get("wid"))
    if result:
        # 同步项目下的任务数量
        synchronous_jobs(worker.get("pid"))
        jid = result.get_jid()
        callbackJson.statusCode = 200
        content["jid"] = jid
        content["log_file_path"] = log_file_path
    return callbackJson.callBacker(content)

if __name__ == "__main__":
    uvicorn.run("logApi:app", host="0.0.0.0", port=50829)