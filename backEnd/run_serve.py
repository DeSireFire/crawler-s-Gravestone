#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/4/11
# CreatTIME : 14:00
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import uvicorn
from server_core.conf import conf, LogLevel
from server_core.hello import hello, logger
from server_core.server import createapp

app = createapp()
if __name__ == "__main__":
    try:
        hello()
        uvicorn.run(app='run_serve:app',
                    host=conf.host,
                    port=conf.port,
                    reload=True,
                    log_level=LogLevel.lower(),
                    log_config="server_core/UlogConf.json"
                    )
    except:
        logger.exception("服务异常！")
