#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/6/18
# CreatTIME : 11:40
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from apps import db_Base
from datetime import datetime
from utils.other import get_md5
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, TEXT, JSON
from sqlalchemy.sql import func


class BaseJson:
    def json(self):
        tdict = self.__dict__
        if "_sa_instance_state" in tdict:
            del tdict["_sa_instance_state"]
        return tdict


class ProjectInfos(db_Base, BaseJson):
    __tablename__ = 'project_infos'
    id = Column(Integer, primary_key=True)
    pid = Column(String(64), unique=True)
    name = Column(String(255))
    nickname = Column(String(255))  # 用于展示的名称，由于存在项目名称重命名的情况
    author = Column(String(64))
    description = Column(String, nullable=False)
    extra = Column(JSON, nullable=True)
    create_time = Column(DateTime(), default=datetime.now(), server_default=func.now())
    update_time = Column(DateTime(), default=datetime.now(), onupdate=func.now())

    def __init__(self, pid=None, name=None, nickname=None, author=None, description=None, extra=None):
        self.pid = pid or get_md5(name)
        self.name = name
        self.nickname = nickname or name
        self.author = author
        self.description = description
        self.extra = extra


class WorkerInfos(db_Base, BaseJson):
    __tablename__ = 'worker_infos'
    id = Column(Integer, primary_key=True)
    wid = Column(String(64), nullable=False)
    pid = Column(String(100), unique=True, nullable=False)
    p_nickname = Column(String(255))
    name = Column(String(255))
    description = Column(String, nullable=False)
    status = Column(String(64))
    modify_user = Column(String(255))
    extra = Column(JSON, nullable=True)
    create_time = Column(DateTime(), default=datetime.now(), server_default=func.now())
    update_time = Column(DateTime(), default=datetime.now(), onupdate=func.now())

    def __init__(self, pid, wid=None, name=None, modify_user=None, description=None, extra=None):
        self.wid = wid or get_md5(f"{name}_{datetime.now().strftime('%Y-%m-%dT%H:%M')}")
        self.pid = pid
        self.name = name
        self.modify_user = modify_user
        self.description = description
        self.extra = extra

__all__ = [
    "ProjectInfos",
    "WorkerInfos",
]
