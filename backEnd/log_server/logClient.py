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
from datetime import datetime
from logging.handlers import HTTPHandler
import socket
import inspect
import json
import os



class CrawlLogUper:
    """

    简单使用实例:

    # 实例化推送器
    obj = CrawlLogUper(
        token="a158dc3a9d0f71283132f2c1127bc8c0",
        log_name="单例爬虫测试日志",
        project_name="高德地图",
        )

    # 定义logger方法
    logger = obj.logger
    # 推送日志信息
    logger.info(f'这是一条 信息 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    logger.error(f'这是一条 错误 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    logger.warning(f'这是一条 警告 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    logger.debug(f'这是一条 调试 日志，发出来测试一下！！！ cpu占用：{cpu}%')

    # 即可
    """
    def __init__(self, token, ip_address="", port="",
                 uper_name="未填写上传者", up_switch=True):
        # 开启是否推送监控信息
        self.up_switch = up_switch if up_switch else False
        # 监控平台的工作流密钥
        self.token = token
        # 推送信息的服务端地址
        self.ip_address = ip_address
        if not self.ip_address:
            self.ip_address = "127.0.0.1"
        # # 推送信息的服务端端口
        self.port = port
        if not self.port:
            self.port = "50829"
        # if not self.port:
        #     self.log_name = f"{__name__} || {inspect.stack()[1][1]}"
        self.handlers = None
        self.uper_name = uper_name
        dn = datetime.now()
        now_ts = int(dn.timestamp() * 1000)
        self.init_mark = str(now_ts)
        self.jid = self.get_job_token()
        self.logger = self.creat_logger(self.jid)

        # print(inspect.stack()[1][1])
        # print(os.path.basename(inspect.stack()[1][1]))

    def creat_logger(self, jid: str = ""):
        assert jid, "任务实例密钥不能为空！"
        _logger = logging.getLogger(jid)
        # print(f"__name__：{__name__}")
        # 用HTTPHandler直接发送日志，而并不是写文件再传文件。
        self.handlers = HTTPHandler(host=f'{self.ip_address}:{self.port}', url='/log', method='POST')
        # 设置日志最低输出级别为无级别，由于logging.NOTSET为0时，日志输出不出去
        _logger.setLevel(logging.NOTSET + 1)
        # 添加Handler对象给记录器（为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方）
        _logger.addHandler(self.handlers)
        return self.extra_logger(_logger, jid)

    def extra_logger(self, _logger, jid=None):
        token = jid if jid else self.jid
        # 添加统一附加信息
        ef = ExtraFilter(self.init_mark, token, jid)
        _logger.addFilter(ef)
        return _logger

    def get_job_token(self, token=None):
        """
        创建任务实例接口提交的数据结构
        'wid': 'a158dc3a9d0f71283132f2c1127bc8c0',
        'run_user': 'admin',

        新增任务实例，并获取任务实例的密钥

        :param self:
        :param token: 工作流密钥
        :return:
        """
        import requests

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7,und;q=0.6,ja;q=0.5',
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://localhost:50831',
            'Referer': 'http://localhost:50831/',
        }

        data = {
            # 'wid': 'a158dc3a9d0f71283132f2c1127bc8c0',
            'wid': token if token else self.token,
            'run_user': self.uper_name,
            # 初始化标记
            'init_mark': self.init_mark,
        }

        response = requests.post(f'http://{self.ip_address}:{self.port}/add_job', headers=headers, data=data)
        assert response.status_code == 200, "链接日志监控平台失败！"
        assert response.json, "日志监控平台响应是发生错误!"
        temp = response.json()
        jid = temp.get("data", {}).get("jid")
        return jid

    def __del__(self):
        try:
            # 关闭推流
            self.logger.removeHandler(self.handlers)
            self.handlers.close()
        except Exception as E:
            print(f"结构销毁是发生了错误：{E}")


class ExtraFilter(logging.Filter):
    def __init__(self, init_mark, token, jid):
        super().__init__()
        self.init_mark = init_mark
        self.token = token
        self.jid = jid

    def filter(self, record):
        extra = {
            'ip': self.get_ip(),
            'init_mark': self.init_mark,
            'token': self.token,
            'jid': self.token,
        }
        record.extra = json.dumps(extra, ensure_ascii=False)
        return True

    @classmethod
    def get_ip(cls):
        ip = socket.gethostbyname(socket.gethostname())
        return ip


# 日志信息模拟
def get_machine_memory_usage_percent():
    """
    获取当前机器cpu占用率
    :return:
    """
    return int(psutil.virtual_memory()._asdict().get('percent'))


if __name__ == '__main__':
    obj = CrawlLogUper(
        token="a158dc3a9d0f71283132f2c1127bc8c0",
        uper_name="tester",
    )
    print(obj.jid)
    logger = obj.logger
    cpu = get_machine_memory_usage_percent()
    logger.info(f'这是一条 信息 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    logger.error(f'这是一条 错误 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    logger.warning(f'这是一条 警告 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    logger.debug(f'这是一条 调试 日志，发出来测试一下！！！ cpu占用：{cpu}%')

    # logger.error(f'这是一条 错误 日志，发出来测试一下！！！ cpu占用：10%')
