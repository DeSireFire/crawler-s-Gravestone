#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/22
# CreatTIME : 15:03
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

# from .models import *
# from .auth import *
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status
from .models import check_password, check_user, UserInDB, Users
from .auth import create_access_token, auth_depend
from fastapi.responses import JSONResponse

route = APIRouter()


# todo 抽取token依赖项
@route.post(
    "/auth_token",
    summary="获取 token 接口",
    description="""采用OAuth2.0认证协议，登录时获取用户的token，
                使用 x-www-form-urlencoded 格式,
                在 Request Body 提交 username 和 password 即可获得本次用户登录的token,
                并会被缓存到 Redis 中保持一定的时间段""",
)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 第一步 拿到 用户名 和密码 ，校验
    username = form_data.username
    password = form_data.password
    # 第二步 通过用户名去数据库中查找到对应的 user
    if not check_user(username):
        err_temp = {
            "err_code": status.HTTP_401_UNAUTHORIZED,
            "err_msg": "登陆失败，用户名与密码不匹配",
            "data": {}
        }
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     # detail="Incorrect username or password",
        #     detail=err_temp,
        #     headers={"WWW-Authenticate": "Bearer"},
        # )
        return err_temp
    # 第三步 检查密码
    if not check_password(username, password):
        err_temp = {
            "err_code": status.HTTP_401_UNAUTHORIZED,
            "err_msg": "登陆失败，用户名与密码还是不匹配",
            "data": {}
        }
        return err_temp
    # 第四步 生成 token
    # Authorization: bearer header.payload.sign
    token = create_access_token({"name": username})
    # 给前端响应信息
    # return {"token": f"bearer {token}"}

    data = {"access_token": token, "token_type": "bearer"}
    temp = {
        "code": 0,
        "message": "OK",
        "data": data,
    }

    return temp


@route.get("/me", summary="个人信息")
async def get_my_info(me: Users = Depends(auth_depend)):
    show_keys = ['name', 'lastlogin', 'nicename', 'role', 'face']
    temp = {k: v for k, v in me.json().items() if k in show_keys} or {}

    return {
        "code": 0,
        "message": "0",
        "ttl": 1,
        "data": temp
    }


@route.get("/demo_err", summary="错误返回演示")
async def error_demo():
    temp = {
        "err_code": "404",
        "err_msg": "一大坨错误信息！",
        "data": {}
    }

    return temp

# @route.post("/auth_token",
#                    summary='登录接口，获取 token',
#                    description="""采用OAuth2.0认证协议，登录时获取用户的token，
#                                 使用 x-www-form-urlencoded 格式,
#                                 在 Request Body 提交 username 和 password 即可获得本次用户登录的token,
#                                 并会被缓存到 Redis 中保持一定的时间段""")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
#                                  mysql_db: Session = Depends(get_mysql_db),
#                                  redis_db: StrictRedis = Depends(get_redis)):
#     user = authenticate_user(mysql_db, form_data.username, form_data.password)  # 查询数据库进行用户验证
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     # 根据 username 生成 token
#     access_token_expires = timedelta(minutes=user_token_conf.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#
#     redis_db.set(access_token, user.username, ex=user_token_conf.ACCESS_TOKEN_EXPIRE_MINUTES * 60)  # 设置 redis_db 缓存
#
#     return Token(
#         code=0,
#         access_token=access_token,
#         token_type='Bearer'
#     )
