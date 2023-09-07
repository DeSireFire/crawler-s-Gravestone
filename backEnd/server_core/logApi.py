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
from datetime import datetime

import pytz

from .log import logger
import uvicorn
from pprint import pprint
from fastapi import FastAPI

from apps.alarms.alarmers_components import AlarmHandler
from apps.projects import get_fetch_one, JobInfos, update_data, WorkerInfos, constructResponse, add_job_one, \
    synchronous_jobs, check_id
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
logger.info(
    "日志接口服务器启动！"
    f"项目根路径：{BASE_DIR}"
)


@app.post("/log2", summary="日志传输接口")
async def log(data: str):
    rdb.set('log', data)
    return {"status": "success"}


# @app.post("/log")
# async def update_logging(request: Request):
#     """
#     接收客户端日志
#     {'args': '()',
#      'created': '1690426537.0822754',
#      'exc_info': 'None',
#      'exc_text': 'None',
#      'extra': '{"ip": "192.168.9.193", "log_name": "单例爬虫测试日志", "project_name": '
#               '"高德地图", "token": "a158dc3a9d0f71283132f2c1127bc8c0"}',
#      'filename': 'logClient.py',
#      'funcName': '<module>',
#      'levelname': 'DEBUG',
#      'levelno': '10',
#      'lineno': '112',
#      'module': 'logClient',
#      'msecs': '82.275390625',
#      'msg': '这是一条 调试 日志，发出来测试一下！！！ cpu占用：57%',
#      'name': '单例爬虫测试日志',
#      'pathname': 'F:\\workSpace\\myGithub\\crawler-s-Gravestone\\backEnd\\log_server\\logClient.py',
#      'process': '15080',
#      'processName': 'MainProcess',
#      'relativeCreated': '146.44455909729004',
#      'stack_info': 'None',
#      'thread': '1028',
#      'threadName': 'MainThread'}
#     {'ip': '192.168.9.193',
#      'log_name': '单例爬虫测试日志',
#      'project_name': '高德地图',
#      'token': 'a158dc3a9d0f71283132f2c1127bc8c0'}
#
#     :param request:
#     :return:
#     """
#     data = await request.body()
#     fdata = await request.form()
#     # 获取日志流传送的信息
#     log_data = fdata.__dict__.get('_dict')
#
#     # 日志附加信息
#     extra_data = json.loads(log_data.get("extra"))
#     # 日志等级
#     log_level = log_data['levelname']
#     # 工作流密钥
#     token = extra_data.get('token', 'unknown')
#     wid = token
#     jid = extra_data.get("jid")
#     j_status = extra_data.get("status") or 0
#     items_count = extra_data.get("items_count") or 0
#     # 预留备用信息传递
#     meta = extra_data.get("meta")
#     try:
#         # 同步到数据库
#         # 获取工作流信息=>
#         # 生成任务实例的jid=>
#         # 通过jid获取任务实例信息，如果没有就生成新的任务实例=>
#
#         # 调用函数并打印结果
#         log_details = create_log_message(log_data)
#         redis_log_key = f"crawl_monitor:logging:{jid}"
#         sub_redis_log_key = f"crawl_monitor:logging:{jid}:{log_level}"
#         rdb.lpush(redis_log_key, log_details.get("log_record"))
#         rdb.lpush(sub_redis_log_key, log_details.get("log_record"))
#
#         # 使用 Redis 的INCR命令对计数器进行原子递增
#         lv_total = count_logs_by_level([log_data])
#
#         # 同步监控数据到数据库
#         job_info = get_fetch_one(JobInfos, jid=jid)
#
#         # 状态
#         # 0 未知，1 执行中，2 结束， 3 中断， 4 失败
#         if j_status:
#             job_info["status"] = j_status
#         else:
#             job_info["status"] = job_info["status"] if job_info["status"] else 3
#
#         # 入库数据计数
#         if job_info["items_count"] == None:
#             job_info["items_count"] = 0
#         if items_count:
#             job_info["items_count"] += items_count or 0
#
#         job_info["log_lv_info"] = lv_total.get(jid, {}).get('INFO') or job_info["log_lv_info"]
#         job_info["log_lv_error"] = lv_total.get(jid, {}).get('ERROR') or job_info["log_lv_error"]
#         job_info["log_lv_warning"] = lv_total.get(jid, {}).get('WARNING') or job_info["log_lv_warning"]
#         job_info["end_time"] = datetime.now(pytz.timezone('Asia/Shanghai'))
#         del job_info["create_time"]
#         job_info_new = update_data(JobInfos, [job_info])
#
#         # 获取日志文件路径
#         log_file_path = job_info.get("log_file_path")
#         logger.info(f"日志保存路径：{log_file_path}")
#         log_to_save(redis_log_key, log_file_path, log_level)
#         # asyncio.run(log_to_save2(redis_log_key, log_file_path))
#
#         # 告警任务推送
#         if log_level == "ERROR":
#             alarm_handler = AlarmHandler()
#             await alarm_handler.handle_alarm(
#                 wid, f'{job_info["name"]}_有关告警信息',
#                 f"该任务接收到了一次报错日志！内容如下:"
#                 f"{log_data['msg']}"
#             )
#
#         # 状态的控制，销毁前发送状态，推送时修改状态，atexit 模块的尝试
#
#         return {"status": "ok", "error": None, "data": data}
#     except Exception as err:
#         logger.error(f"日志流处理错误！错误原因：{err}")
#         return {"status": "err", "error": err, "data": None}


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
    # 工作流密钥
    jid = extra_data.get("jid")
    # 预留备用信息传递
    meta = extra_data.get("meta")
    try:
        # 同步到数据库
        # 获取工作流信息=>
        # 生成任务实例的jid=>
        # 通过jid获取任务实例信息，如果没有就生成新的任务实例=>

        # 同步监控数据到数据库
        job_info = get_fetch_one(JobInfos, jid=jid)
        # 检测任务是否存在
        if not job_info:
            err = f"{jid} 未查询到该任务实例。日志信息明细：{log_data}。 可能是任务被删除。"
            logger.error(err)
            return {"status": "err", "error": err, "data": None}

        # 状态
        await handleStatus(job_info, log_data)

        # 入库数据计数
        await handleItemsCount(job_info, log_data)

        # 日志内容缓存&日志等级统计
        await handleLevelTotal(job_info, log_data)

        # 获取日志文件路径
        await handleLogTextSave(job_info, log_data)

        # 告警任务推送
        await handleAlarm(job_info, log_data)

        # 状态的控制，销毁前发送状态，推送时修改状态，atexit 模块的尝试

        return {"status": "ok", "error": None, "data": data}
    except Exception as err:
        logger.error(f"日志流处理错误！错误原因：{err}")
        return {"status": "err", "error": err, "data": None}


@app.post("/add_job", summary="新增任务")
async def add_job(request: Request, pid: str = Query(None), wid: str = Query(None), jid: str = Query(None)):
    """
    通过传入工作流实例wid等信息创建实际的任务实例记录
    :param request:
    :return:
    """
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
    try:
        # wid 获取工作流信息
        winfo = get_fetch_one(WorkerInfos, wid=data.get("wid"))
        # 没获取到直接返回失败
        if not winfo:
            logger.error(f"所属工作流信息获取失败! 日志创建信息：{data}")
            callbackJson.resData["errMsg"] = "所属工作流信息获取失败！"
            return callbackJson.callBacker(content)

        project_name = winfo.get('name')

        log_file_name = f"{winfo.get('name')}-{init_mark}"
        log_file_path = os.path.join(BASE_DIR, "logs", "worker_logs", project_name, f"{log_file_name}.log")
        data["log_file_path"] = log_file_path
        del data['init_mark']
        # result = add_job_one(JobInfos, data)
        result = handleAddJobOne(JobInfos, data)
        worker = get_fetch_one(WorkerInfos, wid=data.get("wid"))
        if result:
            # 同步项目下的任务数量，还有各项指标参数
            synchronous_jobs(worker.get("pid"))
            jid = result.get_jid()
            callbackJson.statusCode = 200
            content["pid"] = pid
            content["jid"] = jid
            content["log_file_path"] = log_file_path
            # 附加信息，备用传递部分信息到客户端
            content["meta"] = {}
        else:
            err = f"构建新任务实例时失败了，数据明细：{data}"
            logger.error(err)
            callbackJson.message = err
            callbackJson.resData["errMsg"] = err
        return callbackJson.callBacker(content)
    except Exception as e:
        logger.error(f"构建新任务实例时发生了错误！错误原因：{e}")
        callbackJson.statusCode = 400
        callbackJson.message = f"构建新任务实例时发生了错误！错误原因：{e}"
        return callbackJson.callBacker(content)


# 工具函数
async def handleAddJobOne(JobInfos, data):
    """
    新建任务
    :param JobInfos:
    :param data:
    :return:
    """
    try:
        result = add_job_one(JobInfos, data)
        if not check_id(JobInfos, temp_id=result.jid):
            raise ValueError
        return result
    except Exception as e:
        logger.error(f"构建新任务实例时发生了错误！将进行创建重试，错误原因：{e}")
        count = 0
        for i in range(3):
            try:
                count += 1
                result = add_job_one(JobInfos, data)
                if check_id(JobInfos, temp_id=result.jid):
                    return result
            except Exception as ee:
                logger.error(f"构建新任务实例时发生了错误！当前重试次数 ({count})，错误原因：{ee}")

        logger.error(f"构建新任务实例时发生了错误！！重试失败！！！数据明细：{data} 错误原因：{e}")
        return False


async def handleLevelTotal(model_data, log_data):
    """
    处理日志信息等级数量统计
    :param model_data: 需要进行操作的模组查询结果对象
    :param log_data: 日志对象的数据
    :return:
    """
    # 日志附加信息
    extra_data = json.loads(log_data.get("extra"))
    # 日志等级
    log_level = log_data['levelname']
    # 任务id
    jid = extra_data.get("jid")
    # 入库计数
    items_count = extra_data.get("items_count") or 0
    log_details = create_log_message(log_data)
    # 入库计数日志不放在日志等级统计里
    if log_details.get("log_record") != "当前新入库数据1条...":
        logger.info(f"检测到为数据入库计数..pass, items_count:{items_count},msg: {log_details.get('log_record')}")
    else:
        redis_log_key = f"crawl_monitor:logging:{jid}"
        sub_redis_log_key = f"crawl_monitor:logging:{jid}:{log_level}"
        rdb.lpush(redis_log_key, log_details.get("log_record"))
        rdb.lpush(sub_redis_log_key, log_details.get("log_record"))
        # 设置过期时间（以秒为单位，例如，以下设置为 3600 秒，即 1 小时）
        # 避免日志信息在redis中堆积导致溢出
        expire_time = 60 * 60 * 24
        rdb.server.expire(redis_log_key, expire_time)
        rdb.server.expire(sub_redis_log_key, expire_time)

        # 使用 Redis 的INCR命令对计数器进行原子递增
        lv_total = count_logs_by_level([log_data])
        model_data["log_lv_info"] = lv_total.get(jid, {}).get('INFO') or model_data["log_lv_info"]
        model_data["log_lv_error"] = lv_total.get(jid, {}).get('ERROR') or model_data["log_lv_error"]
        model_data["log_lv_warning"] = lv_total.get(jid, {}).get('WARNING') or model_data["log_lv_warning"]
        model_data["end_time"] = datetime.now(pytz.timezone('Asia/Shanghai'))
    del model_data["create_time"]
    model_data_new = update_data(JobInfos, [model_data])


async def handleStatus(model_data, log_data):
    """
    处理任务状态
    :param model_data: 需要进行操作的模组
    :param log_data: 日志对象的数据
    :return:
    """
    # 0 未知，1 执行中，2 结束， 3 中断， 4 失败
    # 日志附加信息
    extra_data = json.loads(log_data.get("extra"))
    j_status = extra_data.get("status") or 0
    if j_status:
        model_data["status"] = j_status
    else:
        model_data["status"] = model_data["status"] if model_data["status"] else 3


async def handleItemsCount(model_data, log_data):
    """
    处理数据入库计数
    :param model: 需要进行操作的模组
    :param log_data: 日志对象的数据
    :return:
    """
    # 日志附加信息
    extra_data = json.loads(log_data.get("extra"))
    items_count = extra_data.get("items_count") or 0
    # 入库数据计数
    if model_data["items_count"] == None:
        model_data["items_count"] = 0
    if items_count:
        model_data["items_count"] += items_count or 0


async def handleLogTextSave(model_data, log_data):
    """
    处理日志文本保存
    :param model: 需要进行操作的模组
    :param log_data: 日志对象的数据
    :return:
    """
    # 日志附加信息
    extra_data = json.loads(log_data.get("extra"))
    # 日志等级
    log_level = log_data['levelname']
    # 任务id
    jid = extra_data.get("jid")
    redis_log_key = f"crawl_monitor:logging:{jid}"
    log_file_path = model_data.get("log_file_path")
    logger.info(f"日志保存路径：{log_file_path}")
    log_to_save(redis_log_key, log_file_path, log_level)
    # 异步写入，有问题
    # asyncio.run(log_to_save2(redis_log_key, log_file_path))


async def handleAlarm(model_data, log_data):
    """
    处理告警业务
    :param model: 需要进行操作的模组
    :param log_data: 日志对象的数据
    :return:
    """
    # 日志附加信息
    extra_data = json.loads(log_data.get("extra"))
    # 日志等级
    log_level = log_data['levelname']
    # 工作流密钥
    token = extra_data.get('token', 'unknown')
    wid = token
    if log_level == "ERROR":
        alarm_handler = AlarmHandler()
        await alarm_handler.handle_alarm(
            wid, f'{model_data["name"]}_有关告警信息',
            f"该任务接收到了一次报错日志！内容如下:"
            f"{log_data['msg']}"
        )


def 测试函数():
    dn = datetime.now()
    now_ts = int(dn.timestamp() * 1000)
    init_mark = str(now_ts)
    data = {
        'wid': 'a158dc3a9d0f71283132f2c1127bc8c0',
        'run_user': "wyx",
        # 初始化标记
        'init_mark': init_mark,
    }

    # wid 获取工作流信息
    winfo = get_fetch_one(WorkerInfos, wid=data.get("wid"))
    project_name = winfo.get('name')
    log_file_name = f"{winfo.get('name')}-{init_mark}"
    log_file_path = os.path.join(BASE_DIR, "logs", "worker_logs", project_name, f"{log_file_name}.log")
    data["log_file_path"] = log_file_path
    del data['init_mark']
    result = add_job_one(JobInfos, data)
    worker = get_fetch_one(WorkerInfos, wid=data.get("wid"))
    print(result)
    print(worker)


if __name__ == "__main__":
    uvicorn.run("logApi:app", host="0.0.0.0", port=50829, workers=5)
    # 测试函数()
