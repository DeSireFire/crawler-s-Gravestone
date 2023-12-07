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
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
import pytz

local_tz = pytz.timezone('Asia/Shanghai')  # 设置所需的时区


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
    customer = Column(String(64))  # 委任方/人
    workers_count = Column(Integer, default=int(0))
    runing_count = Column(Integer, default=int(0))
    description = Column(Text, nullable=False)
    extra = Column(JSON, nullable=True)
    create_time = Column(DateTime(), default=datetime.now(), server_default=func.now())
    update_time = Column(DateTime(), default=datetime.now(), onupdate=func.now())

    def __init__(self, pid=None, name=None, nickname=None, author=None, description=None, extra=None, customer=None):
        self.pid = pid or get_md5(name)
        self.name = name
        self.nickname = nickname or name
        self.author = author
        self.description = description
        self.extra = extra
        self.customer = customer


class WorkerInfos(db_Base, BaseJson):
    __tablename__ = 'worker_infos'
    id = Column(Integer, primary_key=True)
    wid = Column(String(64), unique=True, nullable=False)
    pid = Column(String(100), nullable=False)
    p_nickname = Column(String(255))
    name = Column(String(255), nullable=False)
    nickname = Column(String(255))
    crawl_frequency = Column(Text, nullable=True)
    description = Column(Text, nullable=False)
    status = Column(String(64))
    modify_user = Column(String(255))
    extra = Column(JSON, nullable=True)
    create_time = Column(DateTime(timezone=True), default=datetime.now(), server_default=func.now())
    update_time = Column(DateTime(timezone=True), default=datetime.now(), onupdate=func.now())

    def __init__(self, pid, p_nickname=None, wid=None, name=None, modify_user=None, description=None, extra=None,
                 crawl_frequency=None):
        from apps.projects.components import get_fetch_one
        self.pid = pid
        # self.wid = wid or get_md5(f"{name}_{datetime.now().strftime('%Y-%m-%dT%H:%M')}")
        self.wid = wid or get_md5(f"{name}_{pid}")
        self.name = name
        self.nickname = name
        self.modify_user = modify_user
        self.crawl_frequency = crawl_frequency
        self.description = description
        self.extra = extra
        self.p_nickname = p_nickname if p_nickname else get_fetch_one(model=ProjectInfos, pid=self.pid).get("nickname")
        self.create_time = datetime.now(pytz.timezone('Asia/Shanghai'))
        # self.end_time = datetime.now(pytz.timezone('Asia/Shanghai'))


class JobInfos(db_Base, BaseJson):
    __tablename__ = 'job_infos'
    id = Column(Integer, primary_key=True)
    wid = Column(String(64), nullable=False)
    pid = Column(String(64), nullable=False)
    jid = Column(String(64), nullable=False, unique=True)
    p_nickname = Column(String(255))
    w_nickname = Column(String(255))
    name = Column(String(255), nullable=False, unique=True)
    status = Column(Integer, default=0)  # 0 未知，1 执行中，2 结束， 3 中断， 4 失败
    run_user = Column(String(255))
    log_file_path = Column(Text)
    log_lv_warning = Column(Integer, default=int(0))
    log_lv_error = Column(Integer, default=int(0))
    log_lv_info = Column(Integer, default=int(0))
    log_lv_debug = Column(Integer, default=int(0))
    items_count = Column(Integer, default=int(0))
    extra = Column(JSON, nullable=True)
    create_time = Column(DateTime(timezone=True), default=datetime.now(), server_default=func.now())
    end_time = Column(DateTime(timezone=True), default=datetime.now())

    def __init__(self, wid, pid=None, p_nickname=None, w_nickname=None, jid=None, run_user=None, name=None,
                 log_file_path=None, log_lv_warning=0, log_lv_error=0, log_lv_debug=0, log_lv_info=0, extra=None):
        from apps.projects.components import get_fetch_one
        dn = datetime.now()
        now_time = dn.strftime('%Y-%m-%dT%H:%M:%S')
        now_ts = int(dn.timestamp() * 1000)
        w_info = get_fetch_one(model=WorkerInfos, wid=wid)
        wname = w_info.get("name")
        self.wid = wid
        self.pid = pid
        self.pid = self.pid if self.pid else w_info.get("pid")
        self.p_nickname = p_nickname if p_nickname else get_fetch_one(model=ProjectInfos, pid=self.pid).get("name")
        self.w_nickname = w_nickname if w_nickname else wname
        self.jid = jid or get_md5(f"{wname}_{wid}_{now_time}")
        self.name = name if name else f"{wname}-{now_ts}"
        self.run_user = run_user
        self.log_file_path = log_file_path
        self.log_lv_warning = log_lv_warning
        self.log_lv_error = log_lv_error
        self.log_lv_info = log_lv_info
        self.log_lv_debug = log_lv_debug
        self.extra = extra
        self.create_time = datetime.now(pytz.timezone('Asia/Shanghai'))
        self.end_time = datetime.now(pytz.timezone('Asia/Shanghai'))

    def get_jid(self):
        return self.jid

    def to_dict(self):
        tdict = self.__dict__
        if "_sa_instance_state" in tdict:
            del tdict["_sa_instance_state"]
        return tdict


__all__ = [
    "ProjectInfos",
    "WorkerInfos",
    "JobInfos",
]
