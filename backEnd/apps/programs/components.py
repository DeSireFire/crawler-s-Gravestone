#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/19
# CreatTIME : 11:44
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import os
from datetime import datetime
from utils.other import get_md5
from server_core.log import logger
from server_core.conf import BASE_DIR
from utils.other import get_md5
from utils.shellHelper import ShellCommandExecutor
from utils.gitHelper import GitRepository
from server_core.db import engine, Newsession

# 检查并创建业务日志文件夹
programs_git_path = os.path.join(BASE_DIR, "programs", "git")
if not os.path.exists(programs_git_path):
    os.makedirs(programs_git_path)

# 查唯一键是否存在
def check_id_one(model, **kwargs):
    """
    根据传参字段查询数据是否存在。
    :param model: 需要新增的数据表模组
    :param **kwargs: 不定查询参数 等同于字段
    :return:
    """
    session = Newsession()
    model_data = session.query(model).filter_by(**kwargs).first()
    if model_data:
        return True
    else:
        return False

# 创建任务实例
def add_data_one(model, data):
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


# 获取指定表数据量
def get_query_count(model, **kwargs):
    """
    获取指定表数据量
    :param model: 需要查询的数据表模组
    :return:
    """
    session = Newsession()
    result = session.query(model).filter_by(**kwargs).count() or 0
    return result


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


# 更新批量数据(需要主键)
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



def git_clone(git_url):
    """
    将git仓库的程序克隆到程序管理的位置
    :param git_url: str, 远程仓库地址
    :return:
    """
    programs_path = os.path.join(programs_git_path, "")
    # ShellCommandExecutor("")


__all__ = [
    # 通用性函数
    "get_query_all",
    "get_query_count",
    "get_fetch_one",
    "add_data_one",
    "del_data_one",
    "update_data",
    "check_id_one",
    "ShellCommandExecutor",
    "git_clone",
]
