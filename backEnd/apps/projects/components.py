#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/19
# CreatTIME : 11:44
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from datetime import datetime
from utils.other import get_md5
from .models import ProjectInfos
from server_core.log import logger
from server_core.db import engine, Newsession


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
    old_data = session.query(ProjectInfos).filter_by(pid=data.get("pid")).first()
    if old_data:
        # 灵活赋值
        for key, value in data.items():
            setattr(old_data, key, value)
        old_data.update_time = datetime.now()
    else:
        project_info = ProjectInfos(**data)
        project_info.update_time = datetime.now()
        session.add(project_info)
    try:
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
    "check_pid",
    "del_project_info",
    "add_project_info",
    "update_project_infos",
    "get_projects_info",
]
