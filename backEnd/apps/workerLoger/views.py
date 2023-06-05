#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/30
# CreatTIME : 16:30
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import json
import logging
import os
# from .models import *
# from .auth import *
import time
from datetime import datetime
from urllib.parse import unquote_plus, unquote, parse_qs
from logging.handlers import TimedRotatingFileHandler
from aliyun.log import QueuedLogHandler
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseSettings

from loguru import logger as sub_logger
route = APIRouter()
@route.post("/loguru")
async def update_loguru(request: Request):
    data = await request.body()
    fdata = await request.form()
    # 现在您可以使用 data 变量来访问请求发送来的数据
    log_data = data.decode("utf-8")
    # 日志转换 loguru
    log_record = dict(fdata)
    print(log_record)
    tmp = dict(fdata)
    message = log_record['msg']
    del tmp['levelname']
    del tmp['msg']
    sub_logger.bind(**tmp).log(log_record['levelname'], message)
    vs = [v for k, v in tmp.items()]
    print(" | ".join(vs))
    return {"data": data}

@route.post("/log")
async def update_logging(request: Request):
    data = await request.body()
    fdata = await request.form()
    try:
        record = logrecord(data)
        # print(record)
        file_log_save(record)
        # demo_log_(record)
        # file_logger.log(
        #     int(record.levelno),
        #     record.getMessage()
        # )
        return {"status": "ok", "error": None, "data": data}
    except Exception as err:
        return {"status": "err", "error": err, "data": None}

def logrecord(request_body: bytes):
    """
        接受以字节为单位的请求正文
        并将其转换为LogRecord
        它以url编码的形式出现
        只有安装了标准的logging.handlers.HTTPHandler才能正常工作

        示例传入消息:
            {
                'name': 'main',
                'msg': 'Answer code: 401 request url: GET "http://127.0.0.1:8000/api/v1/user" duration: 74 ms Request body: b\'\' Response body: b\'{"message":"Token expired"}\' ',
                'args': '()',
                'levelname': 'INFO',
                'levelno': '20',
                'pathname': '/app/./app/core/middlewares/logging_middleware.py',
                'filename': 'logging_middleware.py',
                'module': 'logging_middleware',
                'exc_info': 'None',
                'exc_text': 'None',
                'stack_info': 'None',
                'lineno': '155',
                'funcName': '__call__',
                'created': '1647248729.8843582',
                'msecs': '884.3581676483154',
                'relativeCreated': '3603232.8238487244',
                'thread': '140245387786048',
                'threadName': 'MainThread',
                'processName': 'SpawnProcess-2',
                'process': '28'
            }
    """
    assert isinstance(request_body, bytes), 'Request body should be in bytes'
    logrec = unquote(request_body.decode())

    # name=main&process=28...
    log_dict = dict(
        (x.split('=')[0], (x.split('=')[1]))
        for x in logrec.split('&')
    )
    # Заменить + на пробел
    log_dict['msg'] = unquote_plus(log_dict['msg'])
    log_dict['level'] = log_dict['levelno']

    # Если приходят '()' в параметре args, падает в ошибку
    if log_dict.get('args') == '()':
        log_dict['args'] = ''

    temp = record_factory(**log_dict)
    return temp


def record_factory(*args, **kwargs):
    factory = logging.getLogRecordFactory()
    t_record = factory(*args, **kwargs)
    return t_record

class LogSettings(BaseSettings):
    WHEN: str = "D"
    INTERVAL: int = 1
    BACKUP_COUNT: int = 7
    AT_TIME: str = "midnight"
    FORMAT: str = "%(asctime)s : %(levelname)s : %(message)s"
    ROOT: str = "logs"

    class Config:
        env_prefix = "LOG_"
        env_file_encoding = "utf-8"


log_settings = LogSettings()


def get_logger(name):
    logger = logging.getLogger(name)
    # 创建一个handler，用于写入日志文件
    # filename = rf'F:\workSpace\myGithub\crawler-s-Gravestone\backEnd\logs/{datetime.now().date()}_{name}.log'
    filename = f'logs/{datetime.now().date()}_{name}.log'
    fh = logging.FileHandler(filename, mode='a+', encoding='utf-8')
    # 再创建一个handler用于输出到控制台
    ch = logging.StreamHandler()

    # 再再创建一个阿里云sls handler用于输出控制台
    slsh = QueuedLogHandler()

    # 定义输出格式(可以定义多个输出格式例formatter1，formatter2)
    # formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(lineno)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.setLevel(1)

    # 定义日志输出层级
    fh.setLevel(logging.DEBUG)
    # 定义控制台输出层级
    ch.setLevel(logging.WARNING)
    # 定义控制台输出层级
    slsh.setLevel(logging.DEBUG)

    # 为文件操作符绑定格式（可以绑定多种格式例fh.setFormatter(formatter2)）
    fh.setFormatter(formatter)
    # 为控制台操作符绑定格式（可以绑定多种格式例ch.setFormatter(formatter2)）
    ch.setFormatter(formatter)
    # 为控制台操作符绑定格式（可以绑定多种格式例ch.setFormatter(formatter2)）
    # slsh.setFormatter(formatter)

    # 给logger对象绑定文件操作符
    logger.addHandler(fh)
    # 给logger对象绑定文件操作符
    logger.addHandler(ch)
    # 给logger对象绑定sls操作符
    # logger.addHandler(slsh)

    return logger

def file_log_save(record=None):
    """
    将日志流保存到日志文件当中
    :param record:
    :return:
    """
    # temp = {'name': '__main__', 'msg': '这是一条日志，发出来测试一下！！！ cpu占用：50%', 'args': '', 'levelname': 'Level 20', 'levelno': '20', 'pathname': 'F:\\workSpace\\myGithub\\crawler-s-Gravestone\\backEnd\\test\\logerTest.py', 'filename': 'logerTest.py', 'module': 'logerTest', 'exc_info': 'None', 'exc_text': None, 'stack_info': None, 'lineno': '37', 'funcName': None, 'created': 1685603063.502001, 'msecs': 502.0010471343994, 'relativeCreated': 222726.76038742065, 'thread': 26704, 'threadName': 'MainThread', 'processName': 'SpawnProcess-4', 'process': 21112}
    # record = logging.makeLogRecord(temp)
    temp_record = dict(record.__dict__)
    ler = get_logger(temp_record.get("name"))
    # # 写入成功，但是部分参数没有传递
    # ler.log(int(record.levelno), record.getMessage())
    ler.log(int(record.levelno), record.getMessage())

# if __name__ == '__main__':
#     file_log_save()

