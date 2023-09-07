#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/27
# CreatTIME : 11:20
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import asyncio
import io
import json
import os
import time
import logging
import aiofiles
from server_core.conf import redisconf, logger
from utils.RedisDBHelper import RedisDBHelper

rdb = RedisDBHelper(redisconf.db if redisconf.db else 0)
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
        'log_record': log_record.strip()
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
        jid = extra_data.get('jid', 'unknown')
        log_level = log_data['levelname']

        # 构建 Redis key，例如：logs:token1:ERROR
        redis_key = f"crawl_monitor:logging_lv:{jid}:{log_level}"

        # 使用 Redis 的INCR命令对计数器进行原子递增
        redis_client.incr(redis_key)
        # 添加一周的过期时间
        if redis_client.ttl(redis_key) <= 0:
            # 设置过期时间为一个月（30天）
            expire_time = 7 * 24 * 60 * 60
            redis_client.expire(redis_key, expire_time)

    # 获取所有token对应不同level的日志数量
    log_count_by_token = {}
    for key in redis_client.keys("crawl_monitor:logging_lv:*"):
        _n, _l, token, level = key.split(':')
        count = int(redis_client.get(key))
        if token not in log_count_by_token:
            log_count_by_token[token] = {}
        log_count_by_token[token][level] = count

    # todo 待添加过期时间

    return log_count_by_token


def log_to_save(redis_log_key, log_file_path, log_level):
    """
    从redis获取日志数据，保存到log文件
    :param redis_log_key: str,从redis缓存中要读取的
    :param log_file_path: str,日志要保存的路径
    :param log_level: str，日志等级
    :return:
    """
    # 创建目录
    log_directory = os.path.dirname(log_file_path)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # 读取redis
    # elements_to_pop = rdb.server.rpop(redis_log_key)
    # 使用 llen 命令获取列表长度
    list_length = rdb.server.llen(redis_log_key)
    pop_step = -5
    # 存储速度跟不上时动态提高日志内容弹出量
    if list_length > 100:
        pop_step = (list_length//2 + 1) * -1

    # 使用 LRANGE 获取列表中的多个元素（例如，从右端弹出前5个元素）
    elements_to_pop = rdb.server.lrange(redis_log_key, pop_step, -1)
    # 一次性删除多个元素
    rdb.server.ltrim(redis_log_key, 0, -len(elements_to_pop) - 1)

    sub_rkey = f"{redis_log_key}:{log_level}"
    sub_list_length = rdb.server.llen(sub_rkey)
    sub_pop_step = -5
    # 存储速度跟不上时动态提高日志内容弹出量
    if sub_list_length > 100:
        sub_pop_step = (sub_list_length//2 - 1) * -1
    sub_elements_to_pop = rdb.server.lrange(sub_rkey, sub_pop_step, -1)
    # 一次性删除多个元素
    rdb.server.ltrim(redis_log_key, 0, -len(sub_elements_to_pop) - 1)

    # 总日志
    with open(log_file_path, "a+", encoding="utf-8",) as log:
        elements_to_pop = [f"{i}\n" for i in elements_to_pop]
        log.writelines(elements_to_pop)
    # 等级分流日志
    sub_path = rename_log_file(log_file_path, log_level)
    with open(sub_path, "a+", encoding="utf-8",) as log:
        sub_elements_to_pop = [f"{i}\n" for i in sub_elements_to_pop]
        log.writelines(sub_elements_to_pop)

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

async def save_redis_list_to_log(redis_list_key, log_file_path):
    # Create a Redis client
    r = rdb.server

    try:
        # Continue processing until the Redis list is empty
        while True:
            # Use BLPOP to retrieve the first element from the Redis list (FIFO)
            # The function blocks until an item is available to pop
            key, log_data = await asyncio.to_thread(r.blpop, redis_list_key)

            # Convert the log_data to a string (assuming it's a string in the list)
            log_data_str = str(log_data)

            # Use aiofiles to asynchronously open the log file in append mode
            async with aiofiles.open(log_file_path, mode='a') as file:
                # Save the log data to the log file
                await file.write(log_data_str + '\n')

    except asyncio.CancelledError:
        print("异步任务被取消。")
    except Exception as e:
        print("发生错误:", str(e))

async def log_to_save2(redis_list_key, log_file_path):
    log_directory = os.path.dirname(log_file_path)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    task = asyncio.create_task(save_redis_list_to_log(redis_list_key, log_file_path))

    try:
        # Wait for the task to complete
        await task
    except KeyboardInterrupt:
        # Cancel the task if the user interrupts the process
        task.cancel()
        await task

# if __name__ == "__main__":
#     # 替换为你的 Redis 连接信息和 log 文件路径
#     redis_host = "你的_redis主机"
#     redis_port = 6379
#     redis_list_key = "你的_redis_list_key"
#     log_file_path = "你的_log文件路径.log"
#
#     asyncio.run(main(redis_host, redis_port, redis_list_key, log_file_path))


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