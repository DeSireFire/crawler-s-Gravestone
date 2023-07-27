#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/27
# CreatTIME : 14:03
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import uvicorn
from server_core.logApi import app
from server_core.conf import conf, LogLevel
from server_core.hello import logger
if __name__ == '__main__':
    try:
        uvicorn.run(app='run_logServe:app',
                    host=conf.host,
                    port=conf.port-1,
                    reload=True,
                    log_level=LogLevel.lower(),
                    log_config="server_core/UlogConf.json"
                    )
    except:
        logger.exception("服务异常！")
