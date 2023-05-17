#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/4/11
# CreatTIME : 14:00
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
from server_core.log import logger
# from apps.user.user import CurrentUser,CurrentUserRedir
# from fastapi import APIRouter, Depends
#
# route = APIRouter()
#
#
# @logger.catch()
# @route.get("/",summary='测试')
# def login(user : CurrentUser= Depends(CurrentUserRedir)):
#     '''TOKEN 获取接口
#     ============================
#     '''
#     logger.debug(user.username)
#     data = {"msg": "oooooooooooo!", "code": 1,"user":user}
#     return data