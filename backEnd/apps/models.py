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
from sqlalchemy.orm import declarative_base
from server_core.db import engine, Newsession
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()


class Basejson():
    def json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# class Users(Base):
#     __tablename__ = 'users'  # 数据库表名
#
#     username = Column(String(255), primary_key=True, nullable=False, unique=True, index=True)
#     hashed_password = Column(String(255), nullable=False)
#     name = Column(String(255))
#     phone = Column(String(255), nullable=False)


class Users(Base, Basejson):
    __tablename__ = "users"  # 数据库表名

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    password = Column(String(64))
    nicename = Column(String(64))
    role = Column(String(64))
    face = Column(String(255), default='https://i2.hdslb.com/bfs/face/62151cc59344a92a777fddc21119b22956e63e09.jpg@240w_240h_1c_1s.webp')
    status = Column(String(64), default=1)
    create = Column(DateTime(), default=datetime.datetime.now())
    lastlogin = Column(DateTime())

    def __init__(self, name, nicename, password, role, status):
        self.name = name
        self.nicename = nicename
        self.password = password
        self.role = role
        self.status = status
    # def __str__(self):
    #     return self.name


def inituser():
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
    Base.metadata.create_all(engine)
    inituser()
