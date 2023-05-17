#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/10
# CreatTIME : 14:00
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def register_cors(app: FastAPI):
    """
    支持跨域
    """
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=['http://localhost:8081'],  # 有效, 但是本地vue端口一直在变化, 接口给其他人用也不一定是这个端口
        # allow_origins=['*'],   # 无效 bug allow_origins=['http://localhost:8081']
        allow_origin_regex='https?://.*',  # 改成用正则就行了
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

import traceback

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from .log import logger
from starlette.responses import RedirectResponse


class PostParamsError(Exception):
    def __init__(self, err_desc: str="POST请求参数错误"):
        self.err_desc = err_desc


class TokenAuthError(Exception):
    def __init__(self, err_desc: str="token认证失败"):
        self.err_desc = err_desc

class ToLogin(Exception):
    def __init__(self, url: str="/login"):
        self.url = url

class UnicornException(Exception):
    def __init__(self, url: str):
        self.url = url

def register_exception(app: FastAPI):
    """
    全局异常捕获
    """

    @app.exception_handler(ToLogin)
    async def unicorn_exception_handler(request: Request, exc: ToLogin):
        # return JSONResponse(
        #     status_code=418,
        #     content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
        # )
        return RedirectResponse(url=exc.url)


def register_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=['http://localhost:8081'],  # 有效, 但是本地vue端口一直在变化, 接口给其他人用也不一定是这个端口
        # allow_origins=['*'],   # 无效 bug allow_origins=['http://localhost:8081']
        allow_origin_regex='https?://.*',  # 改成用正则就行了
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_middleware(app: FastAPI):
    """
    请求响应拦截 hook

    https://fastapi.tiangolo.com/tutorial/middleware/
    :param app:
    :return:
    """

    @app.middleware("http")
    async def logger_request(request: Request, call_next):
        # https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
        # logger.info(f"访问记录:{request.method} url:{request.url}==headers:{request.headers.get('user-agent')}==IP:{request.client.host}")
        logger.info(f"|访问记录:{request.method}  |url:{request.url}  |IP:{request.client.host}")
        # logger.info(f"|访问记录:{dir(request)}")
        # logger.info(f"|访问记录:{request.headers}")
        response = await call_next(request)
        return response