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
import datetime
import json

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status

from server_core.control import constructResponse
from .components import CRUD
from .models import check_password, check_user, UserInDB, Users, get_users_info, add_user_info, update_user_info, \
    check_uid, del_user_info, get_user_info
from .auth import create_access_token, auth_depend
from fastapi.responses import JSONResponse

route = APIRouter()
sql_crud = CRUD(Users)


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

    # 第四点五 获取用户信息
    user_info = sql_crud.read(name=username, password=password)
    # print(f"user_info.role: {user_info.role}")

    # 给前端响应信息
    data = {
        "role": user_info.role or "normal",
        "access_token": token,
        "token_type": "bearer"
    }
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


@route.get("/get_users")
async def get_users():
    result = get_users_info()
    users = [{k: v for k, v in u.__dict__.items() if not str(k).startswith("_")} for u in result]

    for u in users:
        # u["create"] = json.dumps(u["create"], default=str)
        u["create"] = u["create"].strftime('%Y-%m-%d %H:%M:%S')
        del u['password']

    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {}
    content["list"] = users
    content["pageTotal"] = len(users)
    return callbackJson.callBacker(content)


@route.post("/add_user", summary="新增用户")
async def add_user(request: Request):
    data = await request.body()
    fdata = await request.form()
    user_info = dict(fdata)
    user_info['status'] = 1

    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    if not check_user(user_info.get("name")):
        result = add_user_info(user_info)
        if result:
            callbackJson.statusCode = 200
    return callbackJson.callBacker(content)


@route.post("/edit_user")
async def edit_user(request: Request):
    data = await request.body()
    fdata = await request.form()
    user_info = dict(fdata)
    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    if check_uid(user_info.get("id")):
        result = update_user_info(user_info)
        if result:
            callbackJson.statusCode = 200
    return callbackJson.callBacker(content)


@route.post("/del_user")
async def edit_user(request: Request):
    data = await request.body()
    fdata = await request.form()
    user_info = dict(fdata)
    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    if check_uid(user_info.get("id")):
        result = del_user_info(user_info)
        if result:
            callbackJson.statusCode = 200
    return callbackJson.callBacker(content)


@route.post("/edit_person")
async def edit_person(request: Request):
    """
    用户中心，修改个人密码
    :param request:
    :return:
    """
    data = await request.body()
    fdata = await request.form()
    form_info = dict(fdata)
    callbackJson = constructResponse()
    callbackJson.statusCode = 400
    content = {}
    # 检查用户名是否存在
    if check_user(form_info.get("name")):
        # 获取用户信息
        user_info = get_user_info(form_info.get("name"))
        # 核对旧密码
        if user_info.password == form_info.get("old_password"):
            user_info.password = form_info.get("new_password")
            update_user_info(user_info.to_dict())
            callbackJson.statusCode = 200
        else:
            callbackJson.message = "旧密码不正确！"
    else:
        callbackJson.message = "不存在该用户！"

    return callbackJson.callBacker(content)

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
