#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/17
# CreatTIME : 16:23
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
# 导入项目view
# from apps import user,test
# from apps.user import user, menu
# from apps import test
from apps.route import *
from server_core.middleware import register_cors, register_exception
from server_core.conf import conf


def createapp():
    app = FastAPI(
        title=conf.title,
        description=conf.description,
        version=conf.VERSION,
    )
    # app.mount('/static', StaticFiles(directory='apps/static'), name='static')

    # 用户相关
    app.include_router(users.route, tags=["用户模块"])
    app.include_router(workerLogs.route, tags=["日志收集模块"])
    app.include_router(extras.route, tags=["拓展接口"])
    app.include_router(dashboard.route, tags=["系统首页"])
    app.include_router(projects.route, tags=["项目管理"])

    # @app.get("/")
    # def home():
    #     return RedirectResponse(url="/otdisk/index.html")

    @app.get("/test")
    def test():
        return {"holy": "shit！"}


    # 注册组件
    register_cors(app)  # 跨域设置
    # register_exception(app) # 异常处理

    return app


__all__ = [createapp]