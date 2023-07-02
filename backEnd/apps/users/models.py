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
from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from server_core.db import engine, Newsession
from apps import db_Base

class Basejson():
    def json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Users(db_Base, Basejson):
    __tablename__ = "users"  # 数据库表名

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
    username: str = Field(..., example="test")
    password: str = Field(..., example="123456")


# 模型工具函数

# 检测用户名
def check_user(username=None):
    session = Newsession()
    user = session.query(Users).filter_by(name=username).first()
    if user:
        return True
    else:
        return False


def check_uid(uid=None):
    session = Newsession()
    user = session.query(Users).filter_by(id=uid).first()
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


# 获取数据
def get_user_count():
    session = Newsession()
    user_len = session.query(Users).count() or 0
    return user_len


# 获取所有数据
def get_users_info():
    session = Newsession()
    user = session.query(Users).all()
    if user:
        return user
    else:
        return None


# 新增用户数据
def add_user_info(data):
    session = Newsession()
    user = session.add(Users(**data))
    try:
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False


# 新增用户数据
def update_user_info(data):
    session = Newsession()
    # user = session.query(Users(**data)).filter_by(id=data['id']).first()
    # user.name = data['name']=
    try:
        session.bulk_update_mappings(Users, [data])
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(e)
        return False


# 删除用户数据
def del_user_info(data):
    session = Newsession()
    try:
        user = session.query(Users).filter_by(id=data['id']).first()
        session.delete(user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(e)
        return False
