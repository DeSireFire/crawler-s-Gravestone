#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/6/19
# CreatTIME : 16:32
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
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


def get_machine_memory_usage_percent():
    """
    获取当前机器cpu占用率
    :return:
    """
    return int(psutil.virtual_memory()._asdict().get('percent'))


class MyHTTPHandler(logging.handlers.HTTPHandler):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def __init__(self, host, url, method="GET", secure=False, credentials=None,
                 context=None, **kwargs):
        """
        Initialize the instance with the host, the request URL, and the method
        ("GET" or "POST")
        """
        super().__init__(
            host=host, url=url, method=method, secure=secure, credentials=credentials, context=context,
        )
        self.kwargs = kwargs

    def emit(self, record):
        try:
            if self.method == 'POST':
                headers = {'Content-Type': 'application/json'}
                data = self.format(record)
                requests.post(self.host + self.url, headers=headers, data=data)
            else:
                requests.get(self.host + self.url)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

def save():
    ip_address = "127.0.0.1"
    port = "50830"
    # 生成一个log实例，如果括号为空则返回root logger
    logger = logging.getLogger(__name__)
    print(f"__name__：{__name__}")
    # 用HTTPHandler直接发送日志，而并不是写文件再传文件。
    hh = MyHTTPHandler(host=f'{ip_address}:{port}', url='/log', method='POST')
    # 设置日志最低输出级别为无级别，由于logging.NOTSET为0时，日志输出不出去
    logger.setLevel(logging.NOTSET+1)
    # 添加Handler对象给记录器（为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方）
    logger.addHandler(hh)
    # 获取当前机器cpu占用率
    cpu = get_machine_memory_usage_percent()
    for i in range(1, 101):
        logger.info(
            f'这是一条 信息 日志，发出来测试一下！！！ cpu占用：{cpu}%'
        )
        logger.error(
            f'这是一条 错误 日志，发出来测试一下！！！ cpu占用：{cpu}%'
        )
        logger.warning(
            f'这是一条 警告 日志，发出来测试一下！！！ cpu占用：{cpu}%'
        )
        logger.debug(
            f'这是一条 调试 日志，发出来测试一下！！！ cpu占用：{cpu}%'
        )
        # 输出日志，内容为‘存入600元'
        print(f"运行完毕！{i}次！")
        time.sleep(3)


if __name__ == '__main__':
    save()

# if __name__ == '__main__':
#     logger = logging.getLogger()
#     ip_address = "127.0.0.1"
#     port = "50830"
#     # 用HTTPHandler直接发送日志，而并不是写文件再传文件。
#     handler = MyHTTPHandler(f'{ip_address}:{port}', '/log', method='POST')
#     # 设置日志最低输出级别为无级别，由于logging.NOTSET为0时，日志输出不出去
#     logger.setLevel(logging.NOTSET + 1)
#     # 添加Handler对象给记录器（为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方）
#     logger.addHandler(handler)
#     # 获取当前机器cpu占用率
#     cpu = get_machine_memory_usage_percent()
#     for i in range(1, 101):
#         logger.info(
#             f'这是一条 信息 日志，发出来测试一下！！！ cpu占用：{cpu}%'
#         )
#         logger.error(
#             f'这是一条 错误 日志，发出来测试一下！！！ cpu占用：{cpu}%'
#         )
#         logger.warning(
#             f'这是一条 警告 日志，发出来测试一下！！！ cpu占用：{cpu}%'
#         )
#         logger.debug(
#             f'这是一条 调试 日志，发出来测试一下！！！ cpu占用：{cpu}%'
#         )
#         # 输出日志，内容为‘存入600元'
#         print(f"运行完毕！{i}次！")
#         time.sleep(3)
#
#     # 关闭推流
#     logger.removeHandler(handler)
