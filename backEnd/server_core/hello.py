#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/10
# CreatTIME : 13:43
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from .conf import conf,mysqlconf,LogLevel
from .log import initlog
from .log import logger
from apps.models import initdb

@logger.catch()
def hello():
    initlog()
    initdb()
    if conf.debug:
        print(f"基础参数：{conf}")
        print(f"数据库：{mysqlconf}")
        # docs = f'接口文档 :  http://{conf.host}:{conf.port}{conf.DOCS_URL}'
    txt = f'''============================================================================

            项目名称 :  {conf.title}           
            开发人员 :  RaXianch
            开发时间 :  2023-05-05 
            当前版本 :  {conf.VERSION}
            接口文档 :  http://{conf.host}:{conf.port}{conf.DOCS_URL}
            启动环境 :  {conf.ENV}  |  DEBUG: {conf.debug}   |    日志级别 {LogLevel}            
============================================================================'''
    print(txt)
    logger.info("启动成功！")


if __name__ == '__main__':
    hello()