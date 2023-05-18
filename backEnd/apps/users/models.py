#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/18
# CreatTIME : 15:44
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import time
import datetime
from sqlalchemy.sql import func
from server_core.log import logger
from sqlalchemy.orm import declarative_base
from server_core.db import engine, Newsession
from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()

class Basejson():
    def json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

class Users(Base, Basejson):
    __tablename__ = "users"   # 数据库表名

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    password = Column(String(64))
    nicename = Column(String(64))
    role = Column(String(64))
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


class UserInDB(BaseModel):
    """ 这个模型是orm模型 """
    username: str
    password: str
    is_superuser: bool = False
    status: bool = True

class UserLogin(BaseModel):
    username: str = Field(..., example="tom")
    password: str = Field(..., example="123")

# 检测用户名
def check_user(username):
    session = Newsession()
    user = session.query(Users).filter_by(name=username).first()
    if user:
        return True
    else:
        return False

# 检测密码
def check_password(username, password):
    session = Newsession()
    user = session.query(Users).filter_by(name=username).first()
    if user and user.password == password:
        return True
    else:
        return False

# 获取数据
def get_user_info(username):
    session = Newsession()
    user = session.query(Users).filter_by(name=username).first()
    if user:
        return user
    else:
        return None

def SQLAlchemy2dict(sa_obj):
    return sa_obj.__dict__