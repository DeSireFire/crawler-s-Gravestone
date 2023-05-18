#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/17
# CreatTIME : 17:30
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from pydantic.main import BaseModel
from pydantic import BaseModel, Field, validator
from .models import *
from .auth import *
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends
route = APIRouter()

@route.post("/login", summary="登录接口")
async def login(form_data: UserLogin = Body(...)):
    # 第一步 拿到 用户名 和密码 ，校验
    username = form_data.username
    password = form_data.password
    # 第二步 通过用户名去数据库中查找到对应的 user
    if not check_user(username):
        return {"msg": "登陆失败，用户名与密码不匹配"}
    # 第三步 检查密码
    if not check_password(username, password):
        return {"msg": "登陆失败，用户名与密码还是不匹配"}

    # 第四步 生成 token
    # Authorization: bearer header.payload.sign
    userData = get_user_info(username)
    token = None
    if userData:
        token = create_access_token(userData.json())

    # 第五步 返回响应信息
    return {"token": f"bearer {token}"}

# @route.get("/me", summary="个人信息")
# async def get_my_info(me: UserInDB = Depends(auth_depend)):
#     user_info = UserInfo(**me.dict())
#     return {"msg": user_info}