#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/18
# CreatTIME : 16:54
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
from datetime import datetime, timedelta
from logging import getLogger

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import json
from server_core.db import rdb
import datetime

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        from datetime import date, datetime
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def fake_create_access_token(data: dict) -> str:
    name = data.get("name")
    encoded_jwt = f"nimadeWhy_{name}_temp_fake"
    rkey = f"bearer:{encoded_jwt}"
    rdb.set(rkey, json.dumps(data, cls=ComplexEncoder, ensure_ascii=True))
    # 一周过期
    rdb.server.expire(rkey, datetime.timedelta(weeks=1))
    return encoded_jwt

from datetime import datetime, timedelta
from logging import getLogger

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseSettings
from .models import get_user_info

class Settings(BaseSettings):
    # debug模式
    debug: bool = True

    # jwt加密的 key
    jwt_secret_key: str = "abcdefghijklmn"
    # jwt加密算法
    jwt_algorithm: str = 'HS256'
    # token过期时间，单位：秒
    jwt_exp_seconds: int = 60 * 60
settings = Settings()


logger = getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(seconds=settings.jwt_exp_seconds)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
#     return encoded_jwt

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode_temp = json.dumps(data.copy(), cls=ComplexEncoder, ensure_ascii=True)
    to_encode = json.loads(to_encode_temp)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.jwt_exp_seconds)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def auth_depend(token: str = Depends(oauth2_scheme)):
    # 1. 解析 token 中的 payload 信息
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        logger.exception("token解码失败")
        raise HTTPException(status_code=401, detail="token已失效，请重新登陆！")
    # 2. 根据 payload 中的信息去数据库中找到对应的用户
    username = payload.get("username")
    user = get_user_info(username)
    if user is None:
        raise HTTPException(status_code=401, detail="认证不通过")
    return user