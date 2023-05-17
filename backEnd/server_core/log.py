#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/4/11
# CreatTIME : 14:00
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from loguru import logger
from .conf import BASE_DIR, conf, LogLevel
import os, sys

log_path = os.path.join(BASE_DIR, 'logs')
log_file = os.path.join(log_path, f'BaseApi.log')
logger.remove()
logger.add(sys.stderr, level=LogLevel)
logger.add(log_file, level=LogLevel)


def initlog():
    if not os.path.exists(log_path):
        os.mkdir(log_path)
