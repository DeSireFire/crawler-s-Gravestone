#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/22
# CreatTIME : 15:04
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import json
import datetime
from logging import getLogger

from server_core.db import rdb
from jose import jwt, JWTError
from .models import get_user_info
from pydantic import BaseSettings
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


class UserTokenConfig(BaseSettings):
    """对用户登录时处理token的相关配置"""
    # debug模式
    debug: bool = True
    # jwt加密的 key
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # 通过命令行 `openssl rand -hex 32` 可以生成该安全密钥
    # jwt加密算法
    ALGORITHM: str = "HS256"
    # token过期时间，单位：秒
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        from datetime import date, datetime
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


# 初始化token设置
token_setting = UserTokenConfig()

logger = getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth_token")


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    # 1. 接收需要生成jwt的数据
    to_encode_temp = json.dumps(data.copy(), cls=ComplexEncoder, ensure_ascii=True)
    to_encode = json.loads(to_encode_temp)
    # 2. 生成密钥过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=token_setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    # 3. 为当生成的jwt的字典添加过期时间
    to_encode.update({"exp": expire})
    # 4. 将字典转成jwt
    encoded_jwt = jwt.encode(to_encode, token_setting.SECRET_KEY, algorithm=token_setting.ALGORITHM)

    # todo 4.5 将密钥添加到redis用于快速校验

    # 5.返回token
    return encoded_jwt


def auth_depend(token: str = Depends(oauth2_scheme)):
    # 1. 解析 token 中的 payload 信息
    try:
        payload = jwt.decode(token, token_setting.SECRET_KEY, algorithms=[token_setting.ALGORITHM])
    except JWTError:
        logger.exception("token解码失败")
        raise HTTPException(status_code=401, detail="token已失效，请重新登陆！")
    # 2. 根据 payload 中的信息去数据库中找到对应的用户
    # 2.5 todo 使用redis缓存快速校验，过期校验
    username = payload.get("name")
    user = get_user_info(username)
    if user is None:
        raise HTTPException(status_code=401, detail="认证不通过")
    return user
