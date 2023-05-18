#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/17
# CreatTIME : 17:58
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from . import route
from pydantic.main import BaseModel
from pydantic import BaseModel, Field, validator
from server_core.db import rdb
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends
# route = APIRouter()

# @route.get("/rkeys", summary='测试数据查询')
# async def rkeys(request: Request):
#     temp = rdb.server.keys()
#     return temp

db = {
    "admin": {
        "username": "admin",
        "password": "123qwe",
    },
    "test": {
        "username": "test",
        "password": "123456",
    },
}

class UserLogin(BaseModel):
    username: str = Field(..., example="tom")
    password: str = Field(..., example="123")

def create_access_token(pw) -> str:
    encoded_jwt = f"nimadeWhy_{pw}"
    return encoded_jwt


@route.post("/login", summary="登录接口")
async def login(form_data: UserLogin = Body(...)):
    # 第一步 拿到 用户名 和密码 ，校验
    username = form_data.username
    password = form_data.password
    # 第二步 通过用户名去数据库中查找到对应的 user
    user = username in db.keys()
    if not user:
        return {"msg": "登陆失败，用户名与密码不匹配"}
    # 第三步 检查密码
    pw = db.get(username, {}).get("password") == password
    print(pw)
    if not pw:
        return {"msg": "登陆失败，用户名与密码还是不匹配"}

    # 第四步 生成 token
    # Authorization: bearer header.payload.sign
    token = create_access_token(password)

    # 第五步 返回响应信息
    return {"token": f"bearer {token}"}

# def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     # 第一步 拿到 用户名 和密码 ，校验
#     username = form_data.username
#     password = form_data.password
#     # 第二步 通过用户名去数据库中查找到对应的 user
#     user = db.get_or_none(username)
#     if user is None:
#         return {"msg": "登陆失败，用户名与密码不匹配"}
#     # 第三步 检查密码
#     if not hash_tool.check_password(user.password, password):
#         return {"msg": "登陆失败，用户名与密码不匹配"}
#     # 第四步 生成 token
#     # Authorization: bearer header.payload.sign
#     token = create_access_token({"username": username})
#     # 给前端响应信息
#     # return {"token": f"bearer {token}"}
#     return {"access_token": token, "token_type": "bearer"}

# @route.post("/user/signIn",summary='用户登录，获取TOKEN')
# def login(request:Request,username: str=Body(...), password: str=Body(...),):
#     '''TOKEN 获取接口
#     ============================
#     '''
#     logger.debug(username)
#     session = Newsession()
#     user= session.query(Users).filter_by(name=username,passwd=md5value(password.encode())).first()
#     logger.debug(user)
#     if user:
#         user.lastlogin = datetime.datetime.now()
#         # logger.debug(user.lastlogin.strftime('%Y-%m-%d %H:%M:%S'))
#         info={"id":user.id,"username":user.name,"nicename":user.nicename,
#               "roles":['admin'],'BtnList':['btn.add', 'btn.del', 'btn.edit', 'btn.link'],
#               "photo":'static/photo/head.jpg',"loginip":request.client.host,"lastlogin":user.lastlogin.strftime('%Y-%m-%d %H:%M:%S')}
#         payload = {
#             "iat": int(time.time()),
#             "exp": int(time.time()) + 86400 * 7,
#             # token签发者
#             'iss': 'zlWang',
#             'data': info,
#             "jti": "4f1g23a12aa"
#         }
#         # 生成token
#         token = jwt.encode(payload, conf.SECRET_KEY, algorithm='HS512', )
#         data = {"msg": "登录成功!", "token": token, "code": 1, "userinfo": info}
#         session.add(user)
#         # session.commit()
#     else:
#         data = {"msg": "登录失败!", "code": -1}
#     return data