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
from .models import ProjectInfos, WorkerInfos
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


# 获取所有项目数据
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


# 创建任务实例
def add_job_one(model, data):
    """
    新增某条数据到任务实例表
    :param model: 需要新增的数据表模组
    :param data: dict,单条需要新增的数据
    :return:
    """
    session = Newsession()
    model_data = session.add(model(**data))
    try:
        session.commit()
        return model(**data)
    except Exception as e:
        session.rollback()
        return False


# 获取所有数据
def get_query_all(model, **kwargs):
    """
    获取某表的所有数据
    :param model: 需要查询的数据表模组
    :return:
    """
    session = Newsession()
    result = session.query(model).filter_by(**kwargs).all()
    if result:
        temps = [{k: v for k, v in u.__dict__.items() if not str(k).startswith("_")} for u in result]
        for u in temps:
            for k, v in u.items():
                if isinstance(v, datetime):
                    u[k] = u[k].strftime('%Y-%m-%d %H:%M:%S')
        return temps
    else:
        return None


# 获取单条数据
def get_fetch_one(model, **kwargs):
    """
    获取某表的所有数据
    :param model: 需要查询的数据表模组
    :return:
    """
    session = Newsession()
    result = session.query(model).filter_by(**kwargs).first()
    data = {}
    if result:
        temps = {k: v for k, v in result.__dict__.items() if not str(k).startswith("_")}
        for k, v in temps.items():
            if isinstance(v, datetime):
                data[k] = temps[k].strftime('%Y-%m-%d %H:%M:%S')
            else:
                data[k] = v
        return data
    else:
        return None


# 新增数据
def add_data_one(model, data):
    """
    新增某条数据到某表
    :param model: 需要新增的数据表模组
    :param data: dict,单条需要新增的数据
    :return:
    """
    session = Newsession()
    model_data = session.add(model(**data))
    try:
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False


# 删除数据
def del_data_one(model, **kwargs):
    """
    删除某条数据
    :param model: 需要进行删除操作的数据表
    :param kwargs: dict, 单条需要删除的数据
    :return:
    """
    session = Newsession()
    try:
        fetch_one = session.query(model).filter_by(**kwargs).first()
        session.delete(fetch_one)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(e)
        return False


# 更新数据
def update_data(model, datas):
    """
    批量更新数据
    :param model: 需要进行删除操作的数据表
    :param datas: list, 多条数据列表
    :return:
    """
    session = Newsession()
    try:
        session.bulk_update_mappings(model, datas)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(e)
        return False


# 检查项目的ID是否存在
def check_id(model, temp_id=None):
    session = Newsession()
    data = session.query(model).filter_by(pid=temp_id).first()
    if temp_id and data:
        return True
    else:
        return False


__all__ = [
    "check_pid",
    "check_id",
    "del_project_info",
    "add_project_info",
    "update_project_infos",
    "get_projects_info",
    "add_job_one",
    # 通用性函数
    "get_query_all",
    "get_fetch_one",
    "add_data_one",
    "del_data_one",
    "update_data",
]
