#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/6/16
# CreatTIME : 11:01
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import logging
import math
import os
from pprint import pprint
from pydantic import BaseSettings
from urllib.parse import unquote_plus, unquote, parse_qs
from logging.handlers import TimedRotatingFileHandler
from aliyun.log import QueuedLogHandler
from datetime import datetime

# 检查并创建业务日志文件夹
from server_core.conf import BASE_DIR

worker_logs_path = os.path.join(BASE_DIR, "logs", "worker_logs")
if not os.path.exists(worker_logs_path):
    os.makedirs(worker_logs_path)


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

    log_dict['msg'] = unquote_plus(log_dict['msg'])
    log_dict['level'] = log_dict['levelno']

    # 如果 args 参数中的()出现，则会出现错误
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


def get_logger(name, project_name: str = "未知"):
    if not logging.getLogger(name).hasHandlers():
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger(name)

    # logger = logging.getLogger(name)
    logger.propagate = False
    # 创建一个handler，用于写入日志文件
    # filename = rf'F:\workSpace\myGithub\crawler-s-Gravestone\backEnd\logs/{datetime.now().date()}_{name}.log'
    # filename = f'logs/worker_logs/{project_name}/{datetime.now().date()}_{name}.log'
    file_path = os.path.join(BASE_DIR, "logs", "worker_logs", f"{project_name}")
    filename = os.path.join(file_path, f"{datetime.now().date()}_{name}.log")
    # pprint(f"日志保存路径: {filename}")
    # 判断路径是否存在，不存在则创建
    if not os.path.exists(file_path):
        pprint(f"未发现目录，创建目录: {file_path}")
        os.makedirs(file_path)
    fh = logging.FileHandler(filename, mode='a+', encoding='utf-8')
    # 再创建一个handler用于输出到控制台
    ch = logging.StreamHandler()

    # 再再创建一个阿里云sls handler用于输出控制台
    # slsh = QueuedLogHandler()

    # 定义输出格式(可以定义多个输出格式例formatter1，formatter2)
    # formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(lineno)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.setLevel(1)

    # 定义日志输出层级
    fh.setLevel(logging.INFO)
    # 定义控制台输出层级
    # ch.setLevel(logging.WARNING)
    # 定义控制台输出层级
    # slsh.setLevel(logging.DEBUG)

    # 为文件操作符绑定格式（可以绑定多种格式例fh.setFormatter(formatter2)）
    fh.setFormatter(formatter)
    # 为控制台操作符绑定格式（可以绑定多种格式例ch.setFormatter(formatter2)）
    # ch.setFormatter(formatter)
    # 为控制台操作符绑定格式（可以绑定多种格式例ch.setFormatter(formatter2)）
    # slsh.setFormatter(formatter)

    # 给logger对象绑定文件操作符
    logger.addHandler(fh)
    # 给logger对象绑定文件操作符
    # logger.addHandler(ch)
    # 给logger对象绑定sls操作符
    # logger.addHandler(slsh)

    return logger


def file_log_save(record=None, project_name: str = "未知", log_name: str = "未知名称的"):
    """
    将日志流保存到日志文件当中
    :param record:
    :return:
    """
    # temp = {'name': '__main__', 'msg': '这是一条日志，发出来测试一下！！！ cpu占用：50%', 'args': '', 'levelname': 'Level 20', 'levelno': '20', 'pathname': 'F:\\workSpace\\myGithub\\crawler-s-Gravestone\\backEnd\\test\\logerTest.py', 'filename': 'logerTest.py', 'module': 'logerTest', 'exc_info': 'None', 'exc_text': None, 'stack_info': None, 'lineno': '37', 'funcName': None, 'created': 1685603063.502001, 'msecs': 502.0010471343994, 'relativeCreated': 222726.76038742065, 'thread': 26704, 'threadName': 'MainThread', 'processName': 'SpawnProcess-4', 'process': 21112}
    # record = logging.makeLogRecord(temp)
    # temp_record = dict(record.__dict__)
    # ler = get_logger(temp_record.get("name"), project_name)
    ler = get_logger(log_name, project_name)
    # # 写入成功，但是部分参数没有传递
    # ler.log(int(record.levelno), record.getMessage())
    print(f"record.getMessage() ====> {record.getMessage()}")
    if record.getMessage():
        ler.log(int(record.levelno), record.getMessage())
    # ler.disabled = True
    # del ler


def traverse_folder(path):
    """
    遍历指定文件目录
    :param path:
    :return:
    """
    result = {}
    for root, dirs, files in os.walk(path):
        # print(dirs)
        for file in files:
            if file.endswith('.log'):
                file_path = os.path.join(root, file)
                file_id = get_md5(f"{file_path}")
                size = os.path.getsize(file_path)
                size_human_readable = _convert_size(size)
                rel_path = os.path.relpath(file_path, path)
                folder = os.path.basename(root)
                result[file_id] = {
                    'file_id': file_id,
                    'file_name': file,
                    'folder': folder,
                    'folder_full': root,
                    'rel_path': rel_path,
                    'file_path': file_path,
                    'create_time': os.path.getctime(file_path),
                    'modify_time': os.path.getmtime(file_path),
                    'size': size,
                    'size_human_readable': size_human_readable
                }
    return result


def _convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def get_md5(s):
    """
    字符串转md5
    :param s:
    :return:
    """
    import hashlib
    m = hashlib.md5(s.encode())
    res = m.hexdigest()
    return res


def _handle_logfiles(temp_dict: dict = {}):
    """
    将文件字典处理成业务响应数据

    {
        'file_id': file_id,
        'file_name': file,
        'folder': folder,
        'folder_full': root,
        'rel_path': rel_path,
        'file_path': file_path,
        'create_time': os.path.getctime(file_path),
        'modify_time': os.path.getmtime(file_path),
        'size': size,
        'size_human_readable': size_human_readable

    }
    {'file_id': 'e5d7af83d55fa5215811a47923b6755c', 'file_name': '1686906108295.log', 'folder': '企查查',
     'folder_full': 'F:\\workSpace\\myGithub\\crawler-s-Gravestone\\backEnd\\logs\\worker_logs\\企查查',
     'rel_path': '企查查\\1686906108295.log',
     'file_path': 'F:\\workSpace\\myGithub\\crawler-s-Gravestone\\backEnd\\logs\\worker_logs\\企查查\\1686906108295.log',
     'create_time': 1686906151.965502, 'modify_time': 1686906125.805, 'size': 26980, 'size_human_readable': '26.35 KB'}
    :param temp_dict:
    :return:
    """
    cache_datas = {}
    log_projects = []
    if not cache_datas:
        pronames = [
            "高德地图",
            "美团",
            "企查查",
        ]
        datas = {"list": [], "pageTotal": 0}
        for k, v in temp_dict.items():
            lines = {
                "id": k,
                "name": v.get("file_name"),
                "log_project": v.get("folder"),
                "address": "http://192.168.16.15:50831/",
                "remarks": f"无",
                "create_time": v.get("create_time"),
                "modify_time": v.get("modify_time"),
            }
            datas["list"].append(lines)
            if lines["log_project"] and lines["log_project"] not in log_projects:
                log_projects.append(lines["log_project"])
        datas["pageTotal"] = len(datas["list"])
        datas["log_projects"] = log_projects
        cache_datas = datas
    return cache_datas


def is_file_locked(filepath):
    """
    检测文件是否被占用
    :param filepath: 待检测的文件路径
    :return:
    """
    if os.path.exists(filepath):
        try:
            os.rename(filepath, filepath)
            return False
        except OSError as e:
            return True
    else:
        print("File does not exist")

