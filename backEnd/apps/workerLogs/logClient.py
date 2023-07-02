#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/6/19
# CreatTIME : 16:32
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import inspect
import json
import os

"""
日志推流客户端
"""

# 生成并发送日志
import time
import psutil
import logging
import requests
import logging.config
from logging.handlers import HTTPHandler
import socket

class crawlLogUper():
    def __init__(self, ip_address="", port="", log_name="", project_name=""):
        self.ip_address = ip_address
        if not self.ip_address:
            self.ip_address = "127.0.0.1"
        self.port = port
        if not self.port:
            self.port = "50830"
        self.log_name = log_name
        if not self.port:
            self.log_name = f"{__name__} || {inspect.stack()[1][1]}"
        self.handlers = None
        self.project_name = project_name or "test_client_uper"
        self.logger = self.creat_logger(self.log_name)
        # print(inspect.stack()[1][1])
        # print(os.path.basename(inspect.stack()[1][1]))

    def creat_logger(self, log_name: str = "未知"):
        logger = logging.getLogger(log_name)
        # print(f"__name__：{__name__}")
        # 用HTTPHandler直接发送日志，而并不是写文件再传文件。
        self.handlers = HTTPHandler(host=f'{self.ip_address}:{self.port}', url='/log', method='POST')
        # 设置日志最低输出级别为无级别，由于logging.NOTSET为0时，日志输出不出去
        logger.setLevel(logging.NOTSET + 1)
        # 添加Handler对象给记录器（为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方）
        logger.addHandler(self.handlers)
        # 添加统一附加信息
        ef = ExtraFilter(self.log_name, self.project_name)
        logger.addFilter(ef)
        # 创建初始日志信息
        # extra = {
        #     'ip': self.get_ip(),
        #     'log_name': self.log_name,
        #     'project_name': self.project_name,
        #     }
        # logger.info(f'日志初始化...', extra=extra)
        return logger

    def __del__(self):
        try:
            # 关闭推流
            self.logger.removeHandler(self.handlers)
            self.handlers.close()
        except Exception as E:
            print(f"结构销毁是发生了错误：{E}")

def get_machine_memory_usage_percent():
    """
    获取当前机器cpu占用率
    :return:
    """
    return int(psutil.virtual_memory()._asdict().get('percent'))

class ExtraFilter(logging.Filter):
    def __init__(self, log_name, project_name):
        super().__init__()
        self.log_name = log_name
        self.project_name = project_name

    def filter(self, record):
        extra = {
            'ip': self.get_ip(),
            'log_name': self.log_name,
            'project_name': self.project_name,
            }
        record.extra = json.dumps(extra)
        return True

    @classmethod
    def get_ip(cls):
        ip = socket.gethostbyname(socket.gethostname())
        return ip

if __name__ == '__main__':
    obj = crawlLogUper(log_name="单例爬虫测试日志", project_name="高德地图")
    logger = obj.logger
    cpu = get_machine_memory_usage_percent()
    # logger.info(f'这是一条 信息 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    # logger.error(f'这是一条 错误 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    logger.warning(f'这是一条 浸膏111 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    logger.warning(f'这是一条 错误222 日志，发出来测试一下！！！ cpu占用：{cpu}%')
