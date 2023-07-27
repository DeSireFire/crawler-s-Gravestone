#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/26
# CreatTIME : 18:04
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import json
import uvicorn
from pprint import pprint
from fastapi import FastAPI

from apps.projects import get_fetch_one, JobInfos, update_data, WorkerInfos, constructResponse, add_job_one
from server_core.conf import redisconf
from utils.RedisDBHelper import RedisDBHelper
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, APIRouter, Body, Depends, status, Query
from log_server.components import create_log_message, count_logs_by_level
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
    # print(f"接收到日志数据fdata===>{fdata}")
    log_data = fdata.__dict__.get('_dict')
    log_level = log_data['levelname']
    extra_data = json.loads(log_data.get("extra"))
    token = extra_data.get('token', 'unknown')
    wid = extra_data.get("token")
    try:
        # 同步到数据库
        # 获取工作流信息=>
        # 生成任务实例的jid=>
        # 通过jid获取任务实例信息，如果没有就生成新的任务实例=>
        worker_info = get_fetch_one(WorkerInfos, wid=wid)


        # 调用函数并打印结果
        log_details = create_log_message(log_data)
        rdb.sadd(f"crawl_monitor:logging:{wid}", log_details.get("log_record"))

        # 使用 Redis 的INCR命令对计数器进行原子递增
        lv_total = count_logs_by_level([log_data])


        # job_info["log_lv_info"] = job_info.get(jid, {}).get('INFO')
        # job_info["log_lv_warning"] = job_info.get(jid, {}).get('ERROR')
        # job_info["log_lv_error"] = job_info.get(jid, {}).get('WARNING')
        # job_info_new = update_data(JobInfos, [job_info])

        print(f"lv_total")
        pprint(lv_total)
        print(f"job_info_new")
        # pprint(job_info_new)
        # rdb.incr(f"crawl_monitor:logging_lv:{jid}:{log_level}")
        return {"status": "ok", "error": None, "data": data}
    except Exception as err:
        return {"status": "err", "error": err, "data": None}

@app.post("/add_job", summary="新增任务")
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
    data = await request.body()
    fdata = await request.form()
    data = dict(fdata)

    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    result = add_job_one(JobInfos, data)
    if result:
        jid = result.get_jid()
        callbackJson.statusCode = 200
        content["jid"] = jid
    return callbackJson.callBacker(content)

if __name__ == "__main__":
    uvicorn.run("logApi:app", host="0.0.0.0", port=50829)
