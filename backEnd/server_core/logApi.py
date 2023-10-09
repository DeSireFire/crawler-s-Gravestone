#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/26
# CreatTIME : 18:04
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import os
import pytz
import json
import asyncio
import uvicorn
from pprint import pprint
from starlette.responses import JSONResponse, Response

from .log import logger
from fastapi import FastAPI, HTTPException
from datetime import datetime
from server_core.conf import BASE_DIR
from server_core.conf import redisconf
from utils.RedisDBHelper import RedisDBHelper
from fastapi.middleware.cors import CORSMiddleware
from apps.alarms.alarmers_components import AlarmHandler
from fastapi import Request, APIRouter, Body, Depends, status, Query
from log_server.components import create_log_message, count_logs_by_level, log_to_save, log_file_save
from apps.projects import get_fetch_one, JobInfos, update_data, WorkerInfos, constructResponse, add_job_one, \
    synchronous_jobs, check_id, get_today_job_infos_by_wid, update_status_for_old_jobs, \
    update_status_for_old_comon_jobs, clean_status_for_all_old_jobs, get_long_job_infos_by_wid

# 使用slowapi进行端口频率限制
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

rdb = RedisDBHelper(redisconf.db if redisconf.db else 0)
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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


# 处理速率限制超出的自定义异常处理器
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    callbackJson = constructResponse()
    callbackJson.statusCode = 429
    callbackJson.message = "大圣，收了神通吧..请求速率限制已超出。请稍后再试。"
    return callbackJson.callBacker()


@app.post("/log_total", summary="任务指数统计")
@limiter.limit("5/minute")
async def log_total(request: Request):
    fdata = await request.form()
    data = dict(fdata)
    callbackJson = constructResponse()
    job_info = get_fetch_one(JobInfos, jid=data.get("jid"))
    result = {
        "jid": "",
        "run_user": "",
        "log_lv_warning": 0,
        "log_lv_info": 0,
        "items_count": 0,
        "create_time": 0,
        "end_time": 0,
    }
    for k, v in job_info.items():
        if k in result:
            result[k] = v
    if not result.get("jid"):
        callbackJson.statusCode = 404
    else:
        callbackJson.statusCode = 200

    return callbackJson.callBacker(result)


@app.post("/log", summary="日志传输接口")
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
        job_info = await handleStatus(job_info, log_data)

        # 入库数据计数
        job_info = await handleItemsCount(job_info, log_data)

        # 日志内容缓存&日志等级统计
        job_info = await handleLevelTotal(job_info, log_data)

        # 保存更新数据
        job_info_new = update_data(JobInfos, [job_info])

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
    # 附加信息，备用传递部分信息到客户端
    content["meta"] = {}

    wid = data.get("wid", None)

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

        # wid工作流如果为常驻任务
        # 则判断当日内是否已经创建过同个工作流任务
        # 无则创建，有则直接获取该任务信息，并返回该任务的有关jid
        if winfo.get("crawl_frequency") == "常驻":
            content = await handleAddKeepJob(winfo, data, content)
            if not content.get("jid"):  # 当日没有同个工作流任务，则创建新任务
                content = await handleAddNormalJob(winfo, data, content)
                # 查找前一天相关常驻任务，将其任务状态设为关闭
                update_status_for_old_comon_jobs(wid)

        if winfo.get("crawl_frequency") == "年更":
            # 判断最近2分钟内是否已经出现过同类任务
            # 存在同类任务则直接返回该任务的id
            # 不存在则创建然后返回任务id
            content = await handleAddLongJob(winfo, data, content)
            # 查找前一天相关常驻任务，将其任务状态设为关闭
            update_status_for_old_comon_jobs(wid)


        if winfo.get("crawl_frequency") == "月更":
            pass

        # 当前几个判断获取失败时 content = {'meta': {}}
        # 则按照常规或首次任务进行创建
        if len(content.keys()) == 1:
            # 不是常驻任务，创建新任务
            content = await handleAddNormalJob(winfo, data, content)
            # 查找前一天相关普通任务，修改状态
            update_status_for_old_jobs(wid)
            # todo 异步框架和多线程等因素，会导致多个任务实例创建的整合方法
            # todo 根据创建信息，检测集中的启动时间来判断整合多线程实例
            # todo 接收日志时，发现不识别的密钥，自动根据各项参数，查找当日里多项计数为0的任务实例给安排上

        # todo 检测所有任务(移动到守护程序)
        clean_status_for_all_old_jobs()

        # 错误判断
        # 创建or接续成功，则有jid,没有则任务创建or接续失败！
        if content.get("jid"):
            callbackJson.statusCode = 200
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
async def handleAddLongJob(worker_info, data, content):
    """
    添加年更任务的处理
    :return:
    """
    # 获取工作流id
    wid = data.get("wid")
    # 获取任务时间
    now_ts = data.get("now_time")

    if not now_ts:
        dn = datetime.now()
        now_ts = int(dn.timestamp() * 1000)
    else:
        now_ts = int(now_ts)
    # 获取到符合条件的任务集
    around_jobs = get_long_job_infos_by_wid(wid=wid, now_ts=now_ts, step_time=300)

    if not around_jobs:
        return content

    now_job = around_jobs[0]
    jid = now_job.jid
    pid = now_job.pid
    log_file_path = now_job.log_file_path
    content["pid"] = pid
    content["jid"] = jid
    content["log_file_path"] = log_file_path
    return content

async def handleAddKeepJob(worker_info, data, content):
    """
    添加常驻任务的处理
    :return:
    """
    wid = data.get("wid")
    today_jobs = get_today_job_infos_by_wid(wid=wid)
    # for job in today_jobs:
    #     print(f"job.name: {job.name}")

    if not today_jobs:
        return content

    now_job = today_jobs[0]
    jid = now_job.jid
    pid = now_job.pid
    log_file_path = now_job.log_file_path
    content["pid"] = pid
    content["jid"] = jid
    content["log_file_path"] = log_file_path
    return content


async def handleAddNormalJob(worker_info, data, content):
    """
    添加常规任务的处理
    :return:
    """
    wid = data.get("wid", None)
    init_mark = data.get("init_mark", None)
    project_name = worker_info.get('name')
    log_file_name = f"{worker_info.get('name')}-{init_mark}"
    log_file_path = os.path.join(BASE_DIR, "logs", "worker_logs", project_name, f"{log_file_name}.log")
    data["log_file_path"] = log_file_path
    del data['init_mark']
    del data['now_time']
    # result = add_job_one(JobInfos, data)
    # 新增任务实例到表中
    result = await handleAddJobOne(JobInfos, data)
    if result:
        # 同步项目下的任务数量，还有各项指标参数
        synchronous_jobs(worker_info.get("pid"))
        jid = result.get_jid()
        pid = worker_info.get("pid")
        content["pid"] = pid
        content["jid"] = jid
        content["log_file_path"] = log_file_path
        # 附加信息，备用传递部分信息到客户端
        content["meta"].update({

        })
        print(f"{'*'*20}\n"
              f"新增JID为： {jid} !!!\n"
              f"{'*'*20}\n")
    return content


async def handleAddJobOne(JobInfos, data):
    """
    新建任务
    :param JobInfos:
    :param data:
    :return:
    """
    try:
        result = add_job_one(JobInfos, data)
        # 检测id是否存在于该表，确定创建成功。
        # 不存在则弹出错误，进入重试逻辑
        if not check_id(JobInfos, jid=result.get_jid()):
            raise ValueError
        return result
    except Exception as e:
        logger.error(f"构建新任务实例时发生了错误！将进行创建重试，错误原因：{e}")
        count = 0
        for i in range(3):
            try:
                count += 1
                result = add_job_one(JobInfos, data)
                # 存在则直接返回跳出循环
                if check_id(JobInfos, jid=result.jid):
                    return result
            except Exception as ee:
                logger.error(f"构建新任务实例时发生了错误！当前重试次数 ({count})，错误原因：{ee}")

        logger.error(f"构建新任务实例时发生了错误！！重试失败！！！数据明细：{data} 错误原因：{e}")
        return None

# async def handleAddJobOne(JobInfos, data):
#     """
#     新建任务
#     :param JobInfos:
#     :param data:
#     :return:
#     """
#     try:
#         result = add_job_one(JobInfos, data)
#         # 检测id是否存在于该表，确定创建成功。
#         if not check_id(JobInfos, temp_id=result.jid):
#             raise ValueError
#         return result
#     except Exception as e:
#         logger.error(f"构建新任务实例时发生了错误！将进行创建重试，错误原因：{e}")
#         count = 0
#         for i in range(3):
#             try:
#                 count += 1
#                 result = add_job_one(JobInfos, data)
#                 if check_id(JobInfos, temp_id=result.jid):
#                     return result
#             except Exception as ee:
#                 logger.error(f"构建新任务实例时发生了错误！当前重试次数 ({count})，错误原因：{ee}")
#
#         logger.error(f"构建新任务实例时发生了错误！！重试失败！！！数据明细：{data} 错误原因：{e}")
#         return False


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
    # 解析日志信息为日志对象
    log_details = create_log_message(log_data)
    # 入库计数日志不放在日志等级统计里
    if items_count and "当前新入库数据" in log_details.get("log_record"):
        logger.info(f"检测到为数据入库计数..pass, items_count:{items_count},msg: {log_details.get('log_record')}")
    else:
        redis_log_key = f"crawl_monitor:logging:{jid}"
        sub_redis_log_key = f"crawl_monitor:logging:{jid}:{log_level}"
        rdb.lpush(redis_log_key, log_details.get("log_record"))
        rdb.lpush(sub_redis_log_key, log_details.get("log_record"))
        # 设置过期时间（以秒为单位，例如，以下设置为 3600 秒，即 1 小时）
        # 避免日志信息在redis中堆积导致溢出
        expire_time = 60 * 60
        rdb.server.expire(redis_log_key, expire_time)
        rdb.server.expire(sub_redis_log_key, expire_time)

        # 使用 Redis 的INCR命令对计数器进行原子递增
        lv_total = count_logs_by_level([log_data])
        model_data["log_lv_info"] = lv_total.get(jid, {}).get('INFO') or model_data["log_lv_info"]
        model_data["log_lv_error"] = lv_total.get(jid, {}).get('ERROR') or model_data["log_lv_error"]
        model_data["log_lv_warning"] = lv_total.get(jid, {}).get('WARNING') or model_data["log_lv_warning"]
    model_data["end_time"] = datetime.now(pytz.timezone('Asia/Shanghai'))
    del model_data["create_time"]
    return model_data


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
    return model_data


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
    return model_data


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

    # todo 优化日志弹出方式
    # 从redis获取日志信息保存到日志文件，存在列表弹出过慢，导致日志重复保存的问题
    # 为日后外部程序保存日志提供中间件的函数
    # log_to_save(redis_log_key, log_file_path, log_level)

    # 直接保存日志信息到日志文件
    # 解析日志信息为日志对象
    log_details = create_log_message(log_data)
    log_file_save(log_details, log_file_path, log_level)

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

    # todo 开发占位符，用来替换成各项计数

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
