#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/27
# CreatTIME : 11:20
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import io
import json
import time
import logging
from utils.RedisDBHelper import RedisDBHelper


def create_log_message(log_data):
    """
    将客户端发送的日志信息，转化成可读的
    :param log_data:
    :return:
    """
    # 创建一个基于log_data中log_name的自定义名称的日志记录器
    logger = logging.getLogger(log_data['name'])

    # 将log_data['extra'] JSON字符串转换为字典
    extra_data = json.loads(log_data['extra'])

    # 设置提供的日志格式化器
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 创建一个内存中的StringIO对象以捕获日志输出
    log_buffer = io.StringIO()

    # 创建一个带有自定义格式化器的流处理器
    stream_handler = logging.StreamHandler(log_buffer)
    stream_handler.setFormatter(formatter)

    # 将流处理器添加到日志记录器
    logger.addHandler(stream_handler)

    # 使用log_data['levelno']直接作为日志级别
    log_level = int(log_data['levelno'])

    # 为日志记录器设置日志级别
    logger.setLevel(log_level)

    # 从log_data['created']中获取日志创建时间并格式化为字符串
    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(log_data['created'])))

    # 使用日志记录器创建日志消息
    log_msg = log_data['msg']
    logger.log(log_level, log_msg, extra=extra_data)

    # 移除流处理器以避免重复输出
    logger.removeHandler(stream_handler)

    # 从日志缓冲区获取格式化的日志记录
    log_record = log_buffer.getvalue()

    # 关闭日志缓冲区以释放资源
    log_buffer.close()

    # 将日志消息和其他日志详细信息作为字典返回
    log_details = {
        'log_level': log_level,
        'log_time': log_time,
        'level_name': str(log_data['levelname']),
        'extra': json.loads(log_data['extra']),
        'log_record': log_record.strip()  # Remove trailing newline
    }
    return log_details


# def count_logs_by_level(log_data_list):
#     # 创建一个字典用于存储不同token下不同level的日志数量
#     log_count_by_token = {}
#
#     for log_data in log_data_list:
#         # 解析log_data中的extra字段，获取token和level
#         extra_data = json.loads(log_data['extra'])
#         token = extra_data.get('token', 'unknown')
#         log_level = log_data['levelname']
#
#         # 初始化token下各level的计数器
#         if token not in log_count_by_token:
#             log_count_by_token[token] = {
#                 'ERROR': 0,
#                 'WARNING': 0,
#                 'INFO': 0,
#                 # 可以根据需要添加其他level
#             }
#
#         # 更新对应token和level的日志数量
#         if log_level in log_count_by_token[token]:
#             log_count_by_token[token][log_level] += 1
#
#     return log_count_by_token


def count_logs_by_level(log_data_list):
    # 连接到 Redis 服务器
    redis_client = RedisDBHelper(5).server

    for log_data in log_data_list:
        # 解析log_data中的extra字段，获取token和level
        extra_data = json.loads(log_data['extra'])
        token = extra_data.get('token', 'unknown')
        log_level = log_data['levelname']

        # 构建 Redis key，例如：logs:token1:ERROR
        redis_key = f"crawl_monitor:logging_lv:{token}:{log_level}"

        # 使用 Redis 的INCR命令对计数器进行原子递增
        redis_client.incr(redis_key)

    # 获取所有token对应不同level的日志数量
    log_count_by_token = {}
    for key in redis_client.keys("crawl_monitor:logging_lv:*"):
        _n, _l, token, level = key.split(':')
        count = int(redis_client.get(key))
        if token not in log_count_by_token:
            log_count_by_token[token] = {}
        log_count_by_token[token][level] = count

    return log_count_by_token


if __name__ == '__main__':
    # # 测试数据：提供的日志数据
    # log_data = {
    #     'args': '()',
    #     'created': '1690427500.7859962',
    #     'exc_info': 'None',
    #     'exc_text': 'None',
    #     'extra': '{"ip": "192.168.9.193", "log_name": "单例爬虫测试日志", "project_name": '
    #              '"高德地图", "token": "a158dc3a9d0f71283132f2c1127bc8c0"}',
    #     'filename': 'logClient.py',
    #     'funcName': '<module>',
    #     'levelname': 'ERROR',
    #     'levelno': '40',
    #     'lineno': '110',
    #     'module': 'logClient',
    #     'msecs': '785.9961986541748',
    #     'msg': '这是一条 错误 日志，发出来测试一下！！！ cpu占用：57%',
    #     'name': '单例爬虫测试日志',
    #     'pathname': 'F:\\workSpace\\myGithub\\crawler-s-Gravestone\\backEnd\\log_server\\logClient.py',
    #     'process': '19008',
    #     'processName': 'MainProcess',
    #     'relativeCreated': '526766.8476104736',
    #     'stack_info': 'None',
    #     'thread': '17136',
    #     'threadName': 'MainThread'
    # }
    #
    # # 调用函数并打印结果
    # log_details = create_log_message(log_data)
    # print(log_details)

    # job_add(0)
    pass