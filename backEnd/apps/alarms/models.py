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


class BaseJson:
    def json(self):
        tdict = self.__dict__
        if "_sa_instance_state" in tdict:
            del tdict["_sa_instance_state"]
        return tdict


class Alamers(db_Base, BaseJson):
    """
    id: number | undefined;
    name: string | undefined,
    email: string | undefined,
    qw_token: string | undefined,
    resource: string | undefined,
    desc: string | undefined,
    create_time: string | undefined;
    update_time: string | undefined;
    """
    __tablename__ = 'alamers'
    id = Column(Integer, primary_key=True)
    aid = Column(String(64), unique=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    qw_token = Column(String(255), nullable=True)
    resource = Column(String(255), nullable=False)
    desc = Column(String, nullable=True)
    extra = Column(JSON, nullable=True)
    create_time = Column(DateTime(), default=datetime.now(), server_default=func.now())

    def __init__(self, aid=None, name=None, email=None, qw_token=None, desc=None, extra=None, resource=None):
        self.aid = aid or get_md5(name)
        self.name = name
        self.email = email
        self.qw_token = qw_token
        self.resource = resource
        self.desc = desc
        self.extra = extra


class AlamerJobs(db_Base, BaseJson):
    """
    id: number | undefined;
    a_jid: string | undefined,
    wid: string | undefined,
    aid: string | undefined,
    name: string | undefined,
    resource: string | undefined,
    desc: string | undefined,
    alarm_content: string | undefined,
    extra: string | undefined;
    create_time: string | undefined;
    """
    __tablename__ = 'alamer_jobs'
    id = Column(Integer, primary_key=True)
    a_jid = Column(String(64), unique=True)
    aid = Column(String(64), nullable=False)
    wid = Column(String(64), nullable=False)
    name = Column(String(255), nullable=False)
    resource = Column(String(255), nullable=False)
    desc = Column(String, nullable=True)
    alarm_content = Column(String, nullable=True)
    extra = Column(JSON, nullable=True)
    create_time = Column(DateTime(), default=datetime.now(), server_default=func.now())

    def __init__(self, aid=None, wid=None, a_jid=None, name=None,
                 desc=None, extra=None, resource=None, alarm_content=None
                 ):
        self.aid = aid
        self.wid = wid
        self.a_jid = a_jid or get_md5(f"{resource}_{name}")
        self.name = name
        self.resource = resource
        self.desc = desc
        self.extra = extra
        self.alarm_content = alarm_content


__all__ = [
    "Alamers",
    "AlamerJobs",
]
