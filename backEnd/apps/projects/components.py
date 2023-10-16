#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/19
# CreatTIME : 11:44
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import os
from sqlalchemy import func
from utils.other import get_md5
from server_core.log import logger
from datetime import datetime, timedelta
from server_core.db import engine, Newsession
from .models import ProjectInfos, WorkerInfos, JobInfos

# 检查项目的PID是否存在
def check_pid(name=None, pid=None):
    session = Newsession()
    try:
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
    except Exception as e:
        logger.error(f"{check_pid.__name__} 发生错误：{e}")
        return False
    finally:
        session.close()


# 新增项目数据
def add_project_info(data):
    session = Newsession()
    project = session.add(ProjectInfos(**data))
    try:
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"{add_project_info.__name__} 发生错误：{e}")
        return False
    finally:
        session.close()


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
        logger.error(f"{del_project_info.__name__} 发生错误：{e}")
        return False
    finally:
        session.close()

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
        logger.error(f"{update_project_infos.__name__} 发生错误：{e}")
        return False
    finally:
        session.close()

# 获取所有项目数据
def get_projects_info():
    session = Newsession()
    try:
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
    except Exception as e:
        session.rollback()
        logger.error(f"{get_projects_info.__name__} 发生错误：{e}")
        return False
    finally:
        session.close()


def get_long_job_infos_by_wid(wid, now_ts, step_time):
    """
    查询指定wid下，create_time日期为今天且与now_ts之间的间隔不超过step_time，
    且状态不为 结束 的数据
    :param wid: 工作流ID
    :param now_ts: 时间戳字符串，用于计算间隔时间
    :param step_time: 间隔时间（秒）
    :return: 查询结果的列表，如果找不到则返回空列表
    """
    session = Newsession()
    try:
        now_ts_datetime = datetime.fromtimestamp(int(now_ts)/1000.0)  # 将时间戳字符串转换为 datetime
        delta = timedelta(seconds=step_time)  # 创建时间间隔对象

        # 计算时间范围，以及筛选条件
        start_time = now_ts_datetime - delta
        end_time = now_ts_datetime + delta

        result = session.query(JobInfos).filter_by(wid=wid).filter(
            JobInfos.create_time.between(start_time, end_time),
            JobInfos.status.notin_([2, 4])
        ).all()

        return result
    except Exception as e:
        logger.error(f"get_today_job_infos_by_wid 发生错误：{e}")
        return []
    finally:
        session.close()

def get_today_job_infos_by_wid(wid):
    """
    查询指定wid下，create_time日期为今天的数据
    :param wid: 工作流ID
    :return: 查询结果的列表，如果找不到则返回空列表
    """
    session = Newsession()
    try:
        today = datetime.now().date()  # 获取今天的日期
        result = session.query(JobInfos).filter_by(wid=wid).filter(func.DATE(JobInfos.create_time) == today).all()
        return result
    except Exception as e:
        logger.error(f"get_today_job_infos_by_wid 发生错误：{e}")
        return []
    finally:
        session.close()


def update_status_for_old_comon_jobs(wid, step_day=1):
    """
    常驻类型的历史任务的状态修改
    获取指定wid下昨天和昨天以前且status为0或1的数据，将它们的status转换为对应的新状态，并保存到数据库中
    :param wid: 工作流ID
    """

    session = Newsession()
    try:
        # 计算昨天的日期
        yesterday = datetime.now() - timedelta(days=step_day)

        # 查询指定wid下昨天和昨天以前的数据，status为0或1
        old_jobs = session.query(JobInfos)\
            .filter(JobInfos.wid == wid)\
            .filter(JobInfos.end_time <= yesterday)\
            .filter(JobInfos.status.in_([0, 1]))\
            .all()

        # 更新这些数据的status
        # 0 未知，1 执行中，2 结束， 3 中断， 4 失败
        # 状态未知 改为 中断
        # 状态执行中 改为 结束
        for job in old_jobs:
            if job.status == 1:
                job.status = 2
            else:
                job.status = 3

        # 提交更改
        session.commit()
        logger.info(f"成功更新 {len(old_jobs)} 条数据的 status 为 2")
    except Exception as e:
        session.rollback()  # 回滚事务以防出现错误
        logger.error(f"update_status_to_2_for_old_jobs 发生错误：{e}")
    finally:
        session.close()


def update_status_for_old_jobs(wid):
    """
    普通类型的历史任务的状态修改
    获取指定wid下end_time时间超过一天且状态为0和1的数据
    :param wid: 工作流ID
    """

    session = Newsession()
    try:
        # 计算昨天的日期
        yesterday = datetime.now() - timedelta(days=1)

        # 查询指定wid下昨天和昨天以前的数据，status为0或1
        old_jobs = session.query(JobInfos)\
            .filter(JobInfos.wid == wid)\
            .filter(JobInfos.end_time <= yesterday)\
            .filter(JobInfos.status.in_([0, 1]))\
            .all()

        # 更新这些数据的status
        # 0 未知，1 执行中，2 结束， 3 中断， 4 失败
        # 状态未知 改为 失败
        # 状态执行中 改为 中断
        for job in old_jobs:
            if job.status == 1:
                job.status = 3
            else:
                job.status = 4

        # 提交更改
        session.commit()
        logger.info(f"成功更新 {len(old_jobs)} 条数据的 status 为 2")
    except Exception as e:
        session.rollback()  # 回滚事务以防出现错误
        logger.error(f"update_status_to_2_for_old_jobs 发生错误：{e}")
    finally:
        session.close()


# 创建任务实例
def add_job_one(model, data):
    """
    新增某条数据到任务实例表
    :param model: 需要新增的数据表模组
    :param data: dict,单条需要新增的数据
    :return:
    """
    session = Newsession()
    # 添加是没有返回值的
    temp_model = model(**data)
    try:
        session.add(temp_model)
        session.commit()
        result = session.query(model).filter_by(jid=temp_model.jid).first()
        return result
    except Exception as e:
        session.rollback()
        logger.error(f"{add_job_one.__name__} 发生错误：{e}")
        return False
    finally:
        session.close()


# 获取所有数据
def get_query_all(model, sort_field="", descending=False, **kwargs):
    """
    获取某表的所有数据
    :param descending: 是否按降序排序，默认为 False（正序）
    :param sort_field: str,需要排序的字段
    :param model: 需要查询的数据表模组
    :return:
    """
    session = Newsession()
    try:
        if sort_field:

            if descending:
                result = session.query(model).filter_by(**kwargs).order_by(getattr(model, sort_field).desc()).all()
            else:
                result = session.query(model).filter_by(**kwargs).order_by(getattr(model, sort_field).asc()).all()

        else:
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
        logger.error(f"{get_query_all.__name__} 发生错误：{e}")
        return None
    finally:
        session.close()


# 获取指定表数据量
def get_query_count(model, **kwargs):
    """
    获取指定表数据量
    :param model: 需要查询的数据表模组
    :return:
    """
    session = Newsession()
    try:
        result = session.query(model).filter_by(**kwargs).count() or 0
        return result
    except Exception as e:
        logger.error(f"{get_query_count.__name__} 发生错误：{e}")
        return 0
    finally:
        session.close()



# 获取单条数据
def get_fetch_one(model, **kwargs):
    """
    获取某表的所有数据
    :param model: 需要查询的数据表模组
    :return:
    """
    session = Newsession()
    try:
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
    except Exception as e:
        logger.error(f"{get_fetch_one.__name__} 发生错误：{e}")
        return None
    finally:
        session.close()



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
        logger.error(f"{add_data_one.__name__} 发生错误：{e}")
        return False
    finally:
        session.close()

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
        logger.error(f"{update_data.__name__} 发生错误：{e}")
        return False
    finally:
        session.close()


# 检查项目的ID是否存在
def check_id(model, **filterkw):
    """
    根据指定字段，查询数据是否已存在
    存在返回 true
    不存在和报错返回false
    :param model:
    :param filterkw:
    :return:
    """
    session = Newsession()
    try:
        data = session.query(model).filter_by(**filterkw).first()
        if filterkw and data:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"{check_id.__name__} 发生错误：{e}")
        return False
    finally:
        session.close()


# 根据日志等级修改文件名
def rename_log_file(log_file_path, log_level):
    # 获取原始文件名和扩展名
    original_filename, file_extension = os.path.splitext(os.path.basename(log_file_path))
    # 构建新的文件名：原始文件名 + "_" + log_level + 扩展名
    new_filename = f"{original_filename}_{log_level.lower()}{file_extension}"
    # 获取原始文件所在的文件夹路径
    directory = os.path.dirname(log_file_path)
    # 构建新的文件路径：文件夹路径 + "/" + 新的文件名
    new_file_path = os.path.join(directory, new_filename)
    return new_file_path


# 反向同步部分数据
def synchronous_workers(pid=None):
    """
    同步工作流数量到项目workers_count字段
    :return:
    """
    if pid:
        project_info = get_fetch_one(model=ProjectInfos, pid=pid)
        project_info["workers_count"] = get_query_count(WorkerInfos, pid=pid)
        del project_info["create_time"]
        del project_info["update_time"]
        try:
            pr = update_data(model=ProjectInfos, datas=[project_info])
            return True
        except Exception as E:
            return False
    else:
        workers = get_query_all(WorkerInfos)
        ps = []
        for w in workers:
            pid = w.get("pid") or None
            if pid:
                p = get_fetch_one(model=ProjectInfos, pid=pid)
                p["workers_count"] = get_query_count(WorkerInfos, pid=pid)
                del p["create_time"]
                del p["update_time"]
                ps.append(p)

        if ps:
            try:
                pr = update_data(model=ProjectInfos, datas=ps)
                return True
            except Exception as E:
                return False
        else:
            return False


def synchronous_jobs(pid):
    """
    同步工作流数量到项目workers_count字段
    :return:
    """
    project_info = get_fetch_one(model=ProjectInfos, pid=pid)
    project_info["runing_count"] = get_query_count(JobInfos, pid=pid)
    del project_info["create_time"]
    del project_info["update_time"]
    try:
        pr = update_data(model=ProjectInfos, datas=[project_info])
        return True
    except Exception as E:
        return False

# 读取日志文本最新十行
def read_latest_lines(filename, num_lines=1000):
    """

    # 用法示例
    file_path = 'your_large_file.txt'
    latest_lines = read_latest_lines(file_path, num_lines=1000)
    for line in latest_lines:
        print(line.strip())

    :param filename:
    :param num_lines:
    :return:
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # 如果文件行数不足 num_lines，直接返回所有行
            if len(lines) <= num_lines:
                return lines
            # 否则，返回最新的 num_lines 行
            else:
                return lines[-num_lines:]
    except FileNotFoundError:
        return []





__all__ = [
    "check_pid",
    "check_id",
    "del_project_info",
    "add_project_info",
    "update_project_infos",
    "get_projects_info",
    "add_job_one",
    "synchronous_workers",
    "synchronous_jobs",
    "get_today_job_infos_by_wid",
    "get_long_job_infos_by_wid",
    "update_status_for_old_jobs",
    "update_status_for_old_comon_jobs",

    # 通用性函数
    "get_query_all",
    "get_query_count",
    "get_fetch_one",
    "add_data_one",
    "del_data_one",
    "update_data",
    "rename_log_file",
    "read_latest_lines",
]
