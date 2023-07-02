#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/10
# CreatTIME : 13:36
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import time
import datetime
from sqlalchemy.sql import func
from server_core.log import logger

from server_core.db import engine, Newsession
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey



class Basejson():
    def json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

# 用户初始化，生成特殊用户
def inituser():
    from apps.users.models import Users
    session = Newsession()
    user = session.query(Users).filter_by(name='admin').first()
    if not user:
        adminuser = Users(
            name='admin', nicename="管理员",
            role='admin', password='123qwe',
            status='1'
        )
        session.add(adminuser)
        session.commit()
        session.flush()

    test_user = session.query(Users).filter_by(name='test').first()
    if not test_user:
        adminuser = Users(
            name='test', nicename="测试员",
            role='test', password='123456',
            status='1'
        )
        session.add(adminuser)
        session.commit()
        session.flush()


def initdb():
    from . import db_Base
    # 导入各模块的模组，用于初始化
    from apps.users.models import Users
    from apps.workerLogs.models import worker_logs
    db_Base.metadata.create_all(engine)
    inituser()
