#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/10
# CreatTIME : 14:00
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import os
import sys
import logging
from loguru import logger
from server_core.conf import BASE_DIR, conf, LogLevel

# 后端日志对象
log_path = os.path.join(BASE_DIR, 'logs')
log_file = os.path.join(log_path, f'BaseApi.log')

# 配置Loguru日志
logger.remove()
logger.add(sys.stderr, level=LogLevel)
logger.add(log_file, level=LogLevel, rotation="100 MB", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

# 配置SQLAlchemy日志级别
sqlalchemy_logger = logging.getLogger('sqlalchemy')
sqlalchemy_logger.setLevel(logging.WARNING)  # 设置SQLAlchemy的日志级别为INFO

def initlog():
    if not os.path.exists(log_path):
        os.mkdir(log_path)
