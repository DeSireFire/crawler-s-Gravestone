#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/6/19
# CreatTIME : 16:32
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'


"""
监控信息推流客户端
"""

# 生成并发送日志
import time
import psutil
import logging
import requests
import logging.config
from datetime import datetime
from logging.handlers import HTTPHandler
from logging import StreamHandler
import socket
import inspect
import json
import os
import atexit



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
        self.log_name = f"{__name__} || {inspect.stack()[1][1]}"
        self.http_handlers = None
        self.stream_handler = None
        self.uper_name = uper_name
        dn = datetime.now()
        now_ts = int(dn.timestamp() * 1000)
        self.init_mark = str(now_ts)
        self.log_file_path = None
        self.jid = ""
        if self.up_switch:
            self.jid = self.get_job_token()
        self._logger = None
        self.ef = None      # 过滤器对象
        self.pid = None     # 所属项目pid
        self.meta = {}
        self.logger = self.creat_logger(self.jid)
        # 终止检测
        atexit.register(self.end_point)

        # print(inspect.stack()[1][1])
        # print(os.path.basename(inspect.stack()[1][1]))

    def creat_logger(self, jid: str = ""):
        # assert jid, "任务实例密钥不能为空！"
        # 为空则认为日志推送器为测试状态，不开启推送
        if not jid:
            print("监控信息推流关闭，仅作日志打印..")
            jid = self.log_name
        _logger = logging.getLogger(jid)

        # 设置日志最低输出级别为无级别，由于logging.NOTSET为0时，日志输出不出去
        _logger.setLevel(logging.NOTSET + 1)
        # print(f"__name__：{__name__}")

        # 控制台输出
        self.stream_handler = StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.stream_handler.setFormatter(console_formatter)
        _logger.addHandler(self.stream_handler)
        # print("StreamHandler added:", self.stream_handler in _logger.handlers)

        # 是否推送日志信息
        if self.up_switch:
            # 用HTTPHandler直接发送日志，而并不是写文件再传文件。
            self.http_handlers = HTTPHandler(host=f'{self.ip_address}:{self.port}', url='/log', method='POST')
            # 添加Handler对象给记录器（为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方）
            _logger.addHandler(self.http_handlers)

        self._logger = _logger
        return self.extra_logger(_logger, jid)

    def extra_logger(self, _logger, jid=None):
        token = self.token
        # 添加统一附加信息
        self.ef = ExtraFilter(self.init_mark, token, jid, self.meta, self.pid)
        _logger.addFilter(self.ef)
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
        assert response.status_code == 200, "链接日志监控平台失败！联系管理员！"
        assert response.json, "日志监控平台响应时，发生错误!联系管理员"
        temp = response.json()
        jid = temp.get("data", {}).get("jid")
        self.pid = temp.get("data", {}).get("pid")
        self.log_file_path = temp.get("data", {}).get("log_file_path")
        self.meta = temp.get("data", {}).get("meta", {}) or {}
        return jid

    def items_total(self, items_count=1):
        """
        上传数据入库条数
        :param items_count: int ,用于数据计数
        :return:
        """
        extra = {
            'ip': ExtraFilter.get_ip(),
            'init_mark': self.init_mark,
            'token': self.token,
            'jid': self.jid,
            'pid': self.pid,
            'status': 2,    # 结束
            'items_count': items_count,    # 数据入库计数
            'meta': self.meta,    # 数据入库计数
        }
        self.logger.info(
            f"当前新入库数据{items_count}条...",
            extra=extra
        )

    def remove_handler(self, handler_name):
        # 获取 Logger 中的所有 Handler
        all_handlers = self.logger.handlers

        # 遍历所有 Handler，查找要移除的 Handler
        for handler in all_handlers:
            if handler.get_name() == handler_name:
                # 移除指定的 Handler
                logger.removeHandler(handler)
                print(f"已移除 Handler: {handler_name}")
                break
        else:
            print(f"没有找到名为 {handler_name} 的 Handle")

    def end_point(self):
        """
        程序结束时，执行的函数
        # 0 未知，1 执行中，2 结束， 3 中断， 4 失败
        :return:
        """
        # self._logger.removeHandler(self.ef)
        # logger.removeFilter(self.ef)
        extra = {
            'ip': ExtraFilter.get_ip(),
            'init_mark': self.init_mark,
            'token': self.token,
            'jid': self.jid,
            'pid': self.pid,
            'status': 2,    # 结束
            'items_count': 0,    # 入库数据计数
            'meta': self.meta,    # 入库数据计数
        }
        self.logger.info(
            f"程序执行完毕！",
            extra=extra
        )

    def __del__(self):
        try:
            # 关闭推流
            # self.end_point()
            self.logger.removeHandler(self.http_handlers)
            self.logger.removeHandler(self.stream_handler)
            self.http_handlers.close()
            self.stream_handler.close()
        except Exception as E:
            if self.up_switch:
                print(f"结构销毁是发生了错误：{E}")


class ExtraFilter(logging.Filter):
    def __init__(self, init_mark, token, jid, meta, pid=None):
        super().__init__()
        self.init_mark = init_mark
        self.token = token
        self.jid = jid
        self.meta = meta
        self.pid = pid

    def filter(self, record):
        temp = record.__dict__
        status = 1
        if temp.get("status"):
            status = temp.get("status")
        items_count = temp.get("items_count") if temp.get("items_count", None) else 0
        extra = {
            'ip': self.get_ip(),
            'init_mark': self.init_mark,
            'token': self.token,
            'jid': self.jid,
            'status': status,
            'items_count': items_count,
            'meta': self.meta,
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
        # ip_address="",
        uper_name="tester",
        up_switch=False
    )
    logger = obj.logger
    cpu = get_machine_memory_usage_percent()
    logger.info(f'这是一条 信息 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    # logger.error(f'这是一条 错误 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    # logger.warning(f'这是一条 警告 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    # logger.debug(f'这是一条 调试 日志，发出来测试一下！！！ cpu占用：{cpu}%')
    # for t in range(1, 5):
    #     logger.error(f'这是一条 定时错误 日志，发出来测试一下！！！ cpu占用：10%')
    #     time.sleep(t)

    # obj.items_total()
    # obj.items_total(0)
    # obj.get_job_token()