#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/10
# CreatTIME : 13:43
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
                    workers=4,
                    reload=True,
                    log_level=LogLevel.lower(),
                    log_config="server_core/UlogConf.json"
                    )
    except:
        logger.exception("服务异常！")
