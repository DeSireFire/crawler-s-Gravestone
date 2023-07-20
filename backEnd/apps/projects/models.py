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
from server_core.log import logger
from server_core.db import engine, Newsession
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class BaseJson:
    def json(self):
        tdict = self.__dict__
        if "_sa_instance_state" in tdict:
            del tdict["_sa_instance_state"]
        return tdict


class ProjectInfos(db_Base, BaseJson):
    __tablename__ = 'project_infos'
    id = Column(Integer, primary_key=True)
    pid = Column(String(100), unique=True)
    name = Column(String(255))
    nickname = Column(String(255))  # 用于展示的名称，由于存在项目名称重命名的情况
    author = Column(String(64))
    description = Column(String, nullable=False)
    create_time = Column(DateTime(), default=datetime.now())
    update_time = Column(DateTime(), default=datetime.now())

    def __init__(self, name, author, description):
        self.pid = get_md5(name)
        self.name = name
        self.nickname = name
        self.author = author
        self.description = description


# 检查项目的PID是否存在
def check_pid(name=None, pid=None):
    session = Newsession()
    if name or pid:
        if not pid:
            pid = get_md5(name)
    else:
        return False
    data = session.query(ProjectInfos).filter_by(pid=pid).first()
    if pid and data:
        return True
    else:
        return False


# 新增项目数据
def add_project_info(data):
    session = Newsession()
    project = session.add(ProjectInfos(**data))
    try:
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False


# 删除项目数据
def del_project_info(data):
    session = Newsession()
    try:
        user = session.query(ProjectInfos).filter_by(pid=data['pid']).first()
        session.delete(user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(e)
        return False


# 更新项目数据
def update_project_infos(data):
    session = Newsession()
    try:
        project_info = ProjectInfos(**data)
        project_info.update_time = datetime.now()
        session.merge(project_info)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(e)
        return False


# 获取所有数据
def get_projects_info():
    session = Newsession()
    result = session.query(ProjectInfos).all()
    if result:
        temps = [{k: v for k, v in u.__dict__.items() if not str(k).startswith("_")} for u in result]
        for u in temps:
            for k, v in u.items():
                if isinstance(v, datetime):
                    u[k] = u[k].strftime('%Y-%m-%d %H:%M:%S')
        return temps
    else:
        return None


__all__ = [
    "add_project_info",
    "ProjectInfos",
    "del_project_info",
    "update_project_infos",
    "check_pid",
    "get_projects_info",
]
