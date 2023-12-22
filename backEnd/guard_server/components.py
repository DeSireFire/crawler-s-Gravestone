#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/10/13
# CreatTIME : 11:10
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import re
import os
import io
import json
import time
import pytz
import redis
import asyncio
import logging
import aiofiles
from datetime import datetime
from server_core.db import rdb
from sqlalchemy import func, text
from server_core.db import engine, Newsession
from utils.RedisDBHelper import RedisDBHelper
from server_core.conf import redisconf, logger
from apps.alarms.alarmers_components import AlarmHandler
from apps.projects import get_fetch_one, get_query_all, update_data
from apps.projects.models import ProjectInfos, WorkerInfos, JobInfos
# from log_server.components import create_log_message, count_logs_by_level, log_to_save, log_file_save
from log_server.components import create_log_message, count_logs_by_level


# 将数据表的id数字夯实，减少断续id
def reset_auto_increment_table(table_name):
    logger.info("reset_auto_increment_table 启动,将数据表的id数字夯实，减少断续id...")
    # 创建数据库连接
    session = Newsession()

    # 构建等效的SQL语句
    sql = f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;"

    try:
        # 使用session执行DDL语句
        session.execute(text(sql))
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# redis获取执行前缀的key名称
def get_redis_keys(startWith_key: str):
    if startWith_key:
        rkeys = rdb.server.keys(startWith_key)
    else:
        rkeys = rdb.server.keys()

    return rkeys


# 获取指定jid的job数据
def get_job_by_jid(jid: str):
    return get_fetch_one(model=JobInfos, jid=jid)


# 获取worker数据
def get_workers_all():
    return get_query_all(WorkerInfos)


# 获取结束和失败状态外符合条件的任务
def get_jobs_for_update_job_statuses(wid):
    # 创建数据库连接
    session = Newsession()
    try:
        jobs = session.query(JobInfos).filter(JobInfos.wid == wid, JobInfos.status.notin_([2, 4])).all() or []
        return jobs
    except Exception as e:
        raise e
    finally:
        session.close()


# redis列表弹出指定数量数据,后进先出
def batch_pop_from_redis_list(list_name, batch_size):
    # 使用 lrange 获取要弹出的数据，范围是 [0, batch_size - 1]
    data_to_pop = rdb.server.lrange(list_name, 0, batch_size - 1)

    # 使用 ltrim 命令截取列表，移除已获取的数据
    rdb.server.ltrim(list_name, batch_size, -1)

    return data_to_pop


# redis列表弹出指定数量数据，先进先出
def batch_pop_from_redis_list_fifo(list_name, batch_size: int = -1):
    data_to_pop = []
    # 默认值时，获取全部数据
    if batch_size < 0:
        batch_size = rdb.server.llen(list_name)
    # redis 6.2以下版本的rpop不支持指定数量的弹出
    item = None
    try:
        items = rdb.server.rpop(name=list_name, count=batch_size) or []
        if not items:
            return None
        data_to_pop += items
    except redis.exceptions.ResponseError as rere:
        print(f"Redis 低于6.2版本pop兼容问题,调整为逐个弹出，{rere}.")
        for _ in range(batch_size):
            item = rdb.server.rpop(list_name)
            if item is None:
                break
            data_to_pop.append(item)  # 如果数据是字符串，请根据需要解码
    # 提取时间信息并排序
    sorted_data = sorted(data_to_pop, key=extract_time_info) or []
    return sorted_data


def pop_all_from_redis_list_transaction(list_name):
    # 开启一个 Redis 事务
    pipe = rdb.server.pipeline()

    # 使用 WATCH 命令监视列表，确保在获取和清空期间没有其他操作
    pipe.watch(list_name)

    # 开始事务
    pipe.multi()

    # 使用 lrange 获取列表中的所有元素
    data = pipe.lrange(list_name, 0, -1)

    # 使用 ltrim 清空列表
    pipe.ltrim(list_name, -1, 0)

    # 执行事务
    pipe.execute()

    # 提取时间信息并排序
    sorted_data = sorted(data, key=extract_time_info) or []
    return sorted_data


# 提取日志单行文本开头的时间进行排序
def extract_time_info(log_entry):
    # 使用正则表达式提取时间信息
    time_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', log_entry)
    if time_match:
        time_str = time_match.group(0)
        time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        return time_obj
    return None


# 按日志等级重命名新日志文件名，用于日志分流
def rename_log_file(log_file_path, log_level):
    # 获取原始文件名和扩展名
    original_filename, file_extension = os.path.splitext(os.path.basename(log_file_path))
    # 构建新的文件名：原始文件名 + "_" + log_level + 扩展名
    new_filename = f"{original_filename}_{log_level.lower()}{file_extension}"
    # 获取原始文件所在的文件夹路径
    directory = os.path.dirname(log_file_path)
    # 构建新的文件路径：文件夹路径 + "/" + 新的文件名
    new_file_path = os.path.join(directory, new_filename)
    return new_file_path


def handleLevelTotal(model_data, log_data):
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


def handleStatus(model_data, log_data):
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


def handleItemsCount(model_data, log_data):
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


def handleLogTextSave(model_data, log_data):
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
    # log_details = create_log_message(log_data)
    # log_file_save(log_details, log_file_path, log_level)

    # 异步写入，有问题
    # asyncio.run(log_to_save2(redis_log_key, log_file_path))


def handleAlarm(model_data, log_data):
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
        asyncio.run(
        alarm_handler.handle_alarm(
            wid, f'{model_data["name"]}_有关告警信息',
            f"该任务接收到了一次报错日志！内容如下:"
            f"{log_data['msg']}"
        ))
