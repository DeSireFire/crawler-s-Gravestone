#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/22
# CreatTIME : 15:03
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import json
import logging
import os
# from .models import *
# from .auth import *
from urllib.parse import unquote_plus, unquote
from logging.handlers import TimedRotatingFileHandler

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseSettings

route = APIRouter()


# @route.post("/log", summary="日志上传接口")
# async def log_reception(request: Request, log: str):
#     temp = request.json()
#     print(temp)
#     return temp


@route.post('/log', summary="日志上传接口")
async def get_logs(request: Request):
    """ LogWriter
        Преобразует endpoint в путь к папке с логами
            server.py/dev/app1
        Окончание endpoint-а будет преобразовано в имя файла
        В результате получится:
            /root_dir/dev/app1/app1.log
    """
    root = log_settings.ROOT
    path = request.url.path.strip('/')
    filename = path.split('/')[-1]

    log_path = f"{root}/{path}/{filename}.log"
    log_name = path.replace('/', '_')
    print(f"log_path: {log_path}")
    print(f"log_name: {log_name}")
    if not os.path.isfile(log_path):
        os.makedirs(f"{root}/{path}")

    file_logger = get_logger(log_name, log_path)
    request_body = await request.body()
    print(request_body)
    try:
        record = logrecord(request_body)
        file_logger.log(
            int(record.levelno),
            record.getMessage()
        )
        return {"status": "ok", "error": None, "data": request_body}

    except Exception as err:
        return {"status": "err", "error": err, "data": None}


@route.get('/healthcheck')
async def health():
    return {"status": "ok"}


# 工具函数
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

LOGGING_LEVEL = logging.NOTSET


def get_logger(log_name: str, log_path: str) -> logging.Logger:
    """ Возвращает объект логгер названный точно так же как и принимаемый путь
        dev/app1 -> dev_app1
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(LOGGING_LEVEL)
    log_file_format = "%(asctime)s : %(levelname)s : %(message)s"

    if not logger.hasHandlers():
        # Каждый раз, когда приходит сообщение на логгер навешивается новый экземпляр хэндлера,
        # И каждый хэндлер делает запись в журнале и появляются дубли
        # Чтобы этого не происходило, вставил эту проверку
        fh = TimedRotatingFileHandler(
            log_path,
            when=log_settings.WHEN,
            interval=log_settings.INTERVAL,
            backupCount=log_settings.BACKUP_COUNT,
            atTime=log_settings.AT_TIME,
        )
        fh.setFormatter(logging.Formatter(log_file_format))

        logger.addHandler(fh)
    else:
        fh = TimedRotatingFileHandler(
            log_path,
            when=log_settings.WHEN,
            interval=log_settings.INTERVAL,
            backupCount=log_settings.BACKUP_COUNT,
            atTime=log_settings.AT_TIME,
        )
        fh.setFormatter(logging.Formatter(log_file_format))

        logger.addHandler(fh)

    return logger

# def save_dict_to_log_file(dict_obj, log_file_path):
#     # 使用logging模块将字典存储到log文件中
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.INFO)
#     handler = logging.FileHandler(log_file_path)
#     handler.setLevel(logging.INFO)
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     logger.info(json.dumps(dict_obj))

def logrecord(request_body: bytes):
    """ Принимает тело запроса в байтах
        И преобразует его в LogRecord
        Приходит он в url кодировке
        Это будет работать только если установлен стандартный logging.handlers.HTTPHandler

        Пример входящего сообщения:
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


def demo_log_(log_record):
    import logging.config
    # 采集日志收集对象
    # 配置
    conf = {'version': 1,
            'formatters': {
                'rawformatter': {'class': 'logging.Formatter', 'format': '%(message)s'}
                           },
            'handlers': {'sls_handler': {'()': 'aliyun.log.QueuedLogHandler',
                                         'level': 'INFO',
                                         'formatter': 'rawformatter',

                                         # custom args:
                                         'end_point': os.environ.get('ALIYUN_LOG_SAMPLE_ENDPOINT',
                                                                     'cn-guangzhou.log.aliyuncs.com'),
                                         'access_key_id': os.environ.get('ALIYUN_LOG_SAMPLE_ACCESSID',
                                                                         'xx'),
                                         'access_key': os.environ.get('ALIYUN_LOG_SAMPLE_ACCESSKEY',
                                                                      'xx'),
                                         'project': 'sinohealth-demo',
                                         'log_store': "data_save"
                                         }
                         },
            'loggers': {'sls': {'handlers': ['sls_handler', ],
                                'level': 'INFO',
                                'propagate': False}
                        }
            }
    # 使用
    logging.config.dictConfig(conf)
    crawl_logger = logging.getLogger('sls')
    # print("运行了一次！！")
    # crawl_logger.info("Hello world 5")
    # crawl_logger = FunctionAdapter(crawl_logger, {'func': '测试233'})
    crawl_logger.log(
        level=int(log_record.levelno),
        msg=log_record.getMessage(),
        # extra={
        #     'funcName': log_record.funcName,
        # }
    )
