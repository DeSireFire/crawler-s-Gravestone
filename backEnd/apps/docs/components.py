#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/11/30
# CreatTIME : 15:41
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import uuid
from datetime import datetime
from server_core.log import logger
from apps.users.models import Users
from server_core.db import engine, Newsession
from sqlalchemy.orm.exc import NoResultFound


def generate_unique_id(title):
    """
    根据标题和13位时间戳生成唯一的UUID。

    Parameters:
    - title: 文档标题。

    Returns:
    - unique_id: 生成的唯一标识符。
    """
    # 使用uuid4生成随机UUID
    random_uuid = uuid.uuid4()

    # 获取当前时间的13位时间戳
    timestamp = int(datetime.utcnow().timestamp() * 1000)

    # 将UUID的hex表示和时间戳连接起来
    unique_id = f"{random_uuid.hex}-{timestamp}"

    return unique_id


def get_user_by_author(author_name):
    """
    通过author获取用户信息
    :param title:
    :param author_name:
    :return:
    """
    session = Newsession()
    # 查询用户
    try:
        author = session.query(Users).filter_by(name=author_name).one()
        return author
    except NoResultFound:
        print(f"No user found with name {author_name}")
        return None
    finally:
        # 关闭连接
        session.close()


# 获取所有数据
def get_query_all(model, **kwargs):
    """
    获取某表的所有数据
    :param model: 需要查询的数据表模组
    :return:
    """
    session = Newsession()
    try:
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
    except Exception as e:
        raise e
    finally:
        session.close()


# 获取所有数据
def get_query_docs(model, **kwargs):
    """
    获取某表的所有数据
    :param model: 需要查询的数据表模组
    :return:
    """
    session = Newsession()
    try:
        result = session.query(model).filter_by(**kwargs).all()
        if result:
            temps = []
            for d in result:
                t = {}
                author_json = achmey_to_dict(d.author)
                t['author'] = author_json.get("name") or None
                for k, v in d.__dict__.items():
                    if str(k).startswith("_"):
                        continue
                    if "models" in str(type(v)):
                        continue
                    t[k] = v
                    if isinstance(v, datetime):
                        t[k] = v.strftime('%Y-%m-%d %H:%M:%S')
                temps.append(t)
            return temps
        else:
            return None
    except Exception as e:
        raise e
    finally:
        session.close()


# 将sqlachmey的结果对象转为字典
def achmey_to_dict(achmey_obj):
    if achmey_obj:
        temp = {}
        u = {k: v for k, v in achmey_obj.__dict__.items() if not str(k).startswith("_")}
        for k, v in u.items():
            temp[k] = v
            if isinstance(v, datetime):
                temp[k] = v.strftime('%Y-%m-%d %H:%M:%S')
        return temp
    else:
        return

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
        logger.error(f"{del_data_one.__name__} 发生错误：{e}")
        return False
    finally:
        session.close()