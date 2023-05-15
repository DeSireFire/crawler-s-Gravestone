#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/6
# CreatTIME : 10:32
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

# 生成并发送日志
import logging
import psutil
import time
from logging.handlers import HTTPHandler
import logging.config

def get_machine_memory_usage_percent():
    return int(psutil.virtual_memory()._asdict().get('percent'))

def save():
    logger = logging.getLogger(__name__)
    # 生成一个log实例，如果括号为空则返回root logger
    hh = HTTPHandler(host='127.0.0.1:8000', url='/log', method='POST')
    # 用HTTPHandler直接发送日志，而并不是写文件再传文件。
    logger.setLevel(logging.INFO)
    # 设置日志最低输出级别为info
    logger.addHandler(hh)
    # 添加Handler对象给记录器（为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方）
    demo = get_machine_memory_usage_percent()
    for i in range(1, 101):
        logger.info(
            f'这是一条日志，发出来测试一下！！！ cpu占用：{demo}%'
        )
        # 输出日志，内容为‘存入600元'
        print(f"运行完毕！{i}次！")
        time.sleep(15)


if __name__ == '__main__':
    save()
