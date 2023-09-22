#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/6/27
# CreatTIME : 23:20 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import os
from decimal import Decimal

import psutil
import platform
from datetime import datetime, timedelta

from sqlalchemy import func

from apps.programs import get_query_all
from apps.projects import get_projects_info
from apps.programs.models import ProgramInfos
from apps.projects.models import JobInfos, WorkerInfos, ProjectInfos
from server_core.conf import BASE_DIR
from server_core.db import engine, Newsession

from collections import defaultdict
from sqlalchemy import func
from datetime import datetime, timedelta


def summarize_logs_by_wid(time_range):
    session = Newsession()
    result_list = []
    try:
        # 根据传入的时间范围计算日期范围
        if time_range == 'yesterday':
            old = datetime.now() - timedelta(days=1)
            start_date = datetime(old.year, old.month, old.day-1, 0, 0, 0)
            now = datetime.now()
            end_date = datetime(now.year, now.month, now.day, 0, 0, 0)
            print(f"start_date:{start_date},now：{now}")
        elif time_range == 'last_7_days':
            start_date = datetime.now() - timedelta(days=6)
            end_date = datetime.now()
        elif time_range == 'all_time':
            start_date = datetime.min
            end_date = datetime.now()
        else:
            raise ValueError("Invalid time_range parameter")

        # 查询end_time在指定时间范围内的数据
        job_infos = session.query(JobInfos).filter(
            JobInfos.end_time >= start_date,
            JobInfos.end_time <= end_date
        ).all()

        # 创建一个字典，用于按wid分类和汇总日志级别数据
        wid_logs_summary = defaultdict(lambda: {'wid': None, 'pid': None, 'wname': None, 'pname': None, 'log_sum': 0})

        # 遍历查询结果，根据wid分类并求和日志级别
        for job_info in job_infos:
            wid = job_info.wid
            pid = job_info.pid
            wname = job_info.w_nickname
            pname = job_info.p_nickname
            log_sum = job_info.log_lv_warning + job_info.log_lv_error + job_info.log_lv_info

            # 如果该wid的字典不存在，创建一个新的字典
            if wid_logs_summary[wid]['wid'] is None:
                wid_logs_summary[wid] = {'wid': wid, 'pid': pid, 'wname': wname, 'pname': pname, 'log_sum': log_sum}
            else:
                # 如果字典已存在，更新log_sum字段
                wid_logs_summary[wid]['log_sum'] += log_sum

        # 计算每个wid的log_proportion，即占比
        total_log_sum = sum(item['log_sum'] for item in wid_logs_summary.values())
        for item in wid_logs_summary.values():
            item['log_proportion'] = item['log_sum'] / total_log_sum if total_log_sum > 0 else 0

        # 将结果字典放入列表中，并按log_proportion从大到小排序
        result_list = list(wid_logs_summary.values())
        result_list.sort(key=lambda x: x['log_proportion'], reverse=True)
    except Exception as e:
        print(f"系统首页查询日志统计记录时，发生了错误：{e}")
    finally:
        session.close()
        return result_list



def get_folder_sizes(path):
    """
    获取指定路径下文件夹名称及其文件夹中所有文件的大小，
    以及人类可读的文件大小信息，计算这些文件夹所占总大小的比例。
    最后根据大小比例排序，由大到小的排列。

    Args:
        path (str): 指定路径

    Returns:
        list: 包含文件夹信息的列表，每个元素是一个字典包含以下信息：
              - 'folder_name': 文件夹名称
              - 'size_bytes': 文件夹大小（字节）
              - 'size_human_readable': 人类可读的文件夹大小
              - 'size_ratio': 文件夹大小占总大小的比例
    """
    folder_info_list = []

    # 获取指定路径下所有文件夹
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    # 计算总文件夹大小
    total_size = sum([get_folder_size(os.path.join(path, folder)) for folder in folders])

    # 获取每个文件夹的大小并计算比例
    for folder in folders:
        folder_path = os.path.join(path, folder)
        folder_size = get_folder_size(folder_path)
        size_ratio = folder_size / total_size

        # 将文件夹信息添加到列表中
        folder_info_list.append({
            'folder_name': folder,
            'size_bytes': folder_size,
            'size_human_readable': get_human_readable_size(folder_size),
            'size_ratio': size_ratio
        })

    # 根据大小比例排序
    folder_info_list.sort(key=lambda x: x['size_ratio'], reverse=True)

    return folder_info_list


def get_folder_size(folder_path):
    """
    获取文件夹的大小（字节）。

    Args:
        folder_path (str): 文件夹路径

    Returns:
        int: 文件夹大小（字节）
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size


def get_human_readable_size(size_bytes):
    """
    将字节数转换为人类可读的文件大小表示。

    Args:
        size_bytes (int): 文件大小（字节）

    Returns:
        str: 人类可读的文件大小
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0


def get_completed_jobs():
    """
    查询数据中 status 值为2，且 end_time 超过当前时间10分钟的数据
    :param session: SQLAlchemy session
    :return: List of JobInfos objects
    """
    session = Newsession()
    # 查询状态为2，结束时间在10分钟到一个月之间的数据
    current_time = datetime.now()
    ten_minutes_ago = current_time - timedelta(minutes=10)
    one_month_ago = current_time - timedelta(days=30)
    limit = 10
    # 使用 SQLAlchemy 查询语法进行数据筛选
    result = session.query(JobInfos).filter(
        JobInfos.status == 2,  # 状态值为2
        JobInfos.end_time <= ten_minutes_ago,
        JobInfos.create_time >= one_month_ago
    ).order_by(JobInfos.end_time.desc()).limit(limit)
    datas = []
    if result:
        temps = [{k: v for k, v in u.__dict__.items() if not str(k).startswith("_")} for u in result]
        for u in temps:
            for k, v in u.items():
                if isinstance(v, datetime):
                    u[k] = u[k].strftime('%Y-%m-%d %H:%M:%S')

        has_wid = []

        for d in temps:
            # 将字符串时间转换为datetime对象
            start_time = datetime.strptime(d['create_time'], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(d['end_time'], "%Y-%m-%d %H:%M:%S")
            duration = calculate_duration(start_time, end_time)
            item = {
                "id": d["id"],
                "name": d["name"],
                "status": d["status"],
                "datetime": d["end_time"],
                # "title": f'《{d["name"]}》 任务运行结束! | 结束时间: {d["end_time"]}'
                "title": f'《{d["name"]}》 任务运行结束!',
                "duration": duration,
            }
            datas.append(item)

        session.close()
        return datas
    else:
        session.close()
        return None


def calculate_duration(start_time, end_time):
    """计算耗时，返回耗时时间间隔"""
    if start_time and end_time:
        duration = end_time - start_time
        days = duration.days
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        # 转化为人类可读的时间
        duration_str = ""
        if days > 0:
            duration_str += f"{days}天"
        if hours > 0:
            duration_str += f"{hours}小时"
        if minutes > 0:
            duration_str += f"{minutes}分钟"
        if seconds > 0:
            duration_str += f"{seconds}秒"

        return duration_str if duration_str else "0秒"
        # return duration.total_seconds()  # 返回耗时秒数
    return "未知"


def get_programs_count():
    grams_list = get_query_all(ProgramInfos) or []
    names = [d["name"] for d in grams_list if d["name"]]
    return len(names)


def list_files(path):
    count = 0
    for root, dirs, files in os.walk(path):
        # print(f"info =======> {os.path.join(root)}")
        # print(f"files =======> {files}")
        for file in files:
            if file.endswith('.log'):
                # print(f"info =======> {os.path.join(root, file)}")
                count += 1
    # print(f"count =======> {count}")
    return count


def get_machine_memory_usage_percent():
    """
    获取当前机器cpu占用率
    :return:
    """
    return int(psutil.virtual_memory()._asdict().get('percent'))


def get_yesterday_finish_jobs():
    """
    获取昨日完成任务数量
    :return:
    """
    pro_list = get_projects_info() or []
    names = [d["name"] for d in pro_list if d["name"]]
    return len(names)


def get_yesterday_finish_jobs():
    """
    获取昨日完成的任务数量
    :return:
    """
    session = Newsession()
    try:
        # 获取昨日日期
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_date = yesterday.date()

        # 查询昨日状态为结束(2)的数据数量
        finished_jobs_count = session.query(JobInfos).filter(
            JobInfos.create_time >= yesterday_date,
            JobInfos.create_time < yesterday_date + timedelta(days=1),
            JobInfos.status == 2
        ).count()

        return finished_jobs_count
    except Exception as e:
        print(e)

    finally:
        session.close()


def get_total_jobinfos_count():
    """
    获取任务总数数量
    :param session:
    :return:
    """
    session = Newsession()
    try:
        # 查询JobInfos表的总数据数量
        total_jobinfos_count = session.query(JobInfos).count()

        return total_jobinfos_count
    except Exception as e:
        print(e)

    finally:
        session.close()


def count_logs_modified_yesterday(directory_path):
    """

    # 指定要遍历的文件夹路径
    directory_path = "/path/to/your/log/directory"

    # 调用函数来获取昨日日志文件的数量
    log_count = count_logs_modified_yesterday(directory_path)

    遍历当中的最后修改时间为昨日的log文件，并统计其数量。
    :param directory_path:
    :return:
    """
    # 获取昨日日期
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_date = yesterday.date()

    # 初始化计数器
    log_count = 0

    # 遍历指定目录下的所有文件
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # 检查文件是否是日志文件（您可以根据文件名后缀或其他标识来判断）
            if file_name.endswith(".log"):
                # 获取文件的最后修改时间
                modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                # 检查最后修改时间是否为昨日
                if modification_time.date() == yesterday_date:
                    log_count += 1

    return log_count


def get_running_jobs_count():
    """
    获取正在执行中的任务数量
    :param session:
    :return:
    """
    session = Newsession()
    try:
        # 查询状态为执行中(1)的数据数量
        running_jobs_count = session.query(JobInfos).filter(JobInfos.status == 1).count()

        return running_jobs_count
    except Exception as e:
        print(e)
    finally:
        session.close()


def get_projects_count():
    """
    获取项目数量
    :return:
    """
    pro_list = get_projects_info() or []
    names = [d["name"] for d in pro_list if d["name"]]
    return len(names)


def get_disk_space_percentage():
    """
    获取硬盘剩余空间

    # 调用函数来获取硬盘剩余空间百分比
    free_space_percentage = get_disk_space_percentage()

    # 打印结果
    print(f"硬盘剩余空间百分比：{free_space_percentage:.2f}%")
    :return:
    """
    free_space_percentage = ""
    try:
        if platform.system() == "Linux":
            # 获取Linux系统下硬盘的剩余空间
            disk_usage = psutil.disk_usage('/')
            free_space_percentage = disk_usage.free / disk_usage.total
        elif platform.system() == "Windows":
            # 获取Windows系统下硬盘的剩余空间
            partitions = psutil.disk_partitions()
            for partition in partitions:
                if 'C:' in partition.device:
                    disk_usage = psutil.disk_usage(partition.device)
                    free_space_percentage = disk_usage.free / disk_usage.total
                    break
        else:
            raise Exception("检测系统剩余空间时，发现不支持的操作系统")
    except Exception as e:
        print(e)
    finally:
        # 减去剩余空间即为已用空间
        return 1 - free_space_percentage


def get_items_count_by_wid(wid):
    """
    统计指定工作流所属的所有任务的数据计数总和
    :param wid:
    :return:
    """
    session = Newsession()
    try:
        # 查询wid为指定值的所有数据，并计算items_count总和
        total_items_count = session.query(func.sum(JobInfos.items_count)).filter(
            JobInfos.wid == wid
        ).scalar()

        # 如果没有匹配的数据，则返回0
        if total_items_count is None:
            total_items_count = 0

        if isinstance(total_items_count, Decimal):
            total_items_count = float(total_items_count)

        return total_items_count
    except Exception as e:
        print(e)
    finally:
        session.close()


def get_items_count_by_wid_with_time_limit(wid):
    session = Newsession()
    # 获取昨日日期
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_date = yesterday.date()

    # 查询wid为指定值且在昨日日期内的所有数据，并计算items_count总和
    total_items_count = session.query(func.sum(JobInfos.items_count)).filter(
        JobInfos.wid == wid,
        JobInfos.create_time >= yesterday_date,
        JobInfos.create_time < yesterday_date + timedelta(days=1)
    ).scalar()

    # 如果没有匹配的数据，则返回0
    if total_items_count is None:
        total_items_count = 0

    return total_items_count


from sqlalchemy import desc


def get_latest_job_info_by_wid(wid):
    """
    获取指定工作流最新更新任务的指数统计信息
    :param wid:
    :return:
    """
    session = Newsession()
    res_dict = {}
    try:
        # 查询指定wid值匹配的记录，并按end_time降序排序，选择第一条记录
        latest_job_info = session.query(JobInfos).filter(JobInfos.wid == wid).order_by(desc(JobInfos.end_time)).first()
        res_dict["pid"] = latest_job_info.pid
        res_dict["wid"] = latest_job_info.wid
        res_dict["jid"] = latest_job_info.jid
        res_dict["job_name"] = latest_job_info.name
        res_dict["passing_total"] = latest_job_info.items_count
        res_dict["failure_total"] = latest_job_info.log_lv_warning
        if latest_job_info.items_count and latest_job_info.items_count+latest_job_info.log_lv_warning:
            res_dict["passing_rate"] = latest_job_info.items_count/(latest_job_info.items_count+latest_job_info.log_lv_warning)
        else:
            res_dict["passing_rate"] = 0

        res_dict["history_total"] = get_items_count_by_wid(wid)
        return res_dict
    except Exception as e:
        print(f"get_latest_job_info_by_wid 查询是发生了错误！ {e}")
    finally:
        session.close()

def get_memory_usage():
    """
    获取当前机器内存占用情况
    :return:
    """
    process = psutil.Process()
    memory_info = process.memory_info()

    virtual_memory = psutil.virtual_memory()
    memory_total = {"内存总量": f"{virtual_memory.total / 1024 / 1024 / 1024:.2f} GB",
                    "内存空闲": f"{virtual_memory.available / 1024 / 1024 / 1024:.2f} GB",
                    "内存占用": f"{virtual_memory.used / 1024 / 1024 / 1024:.2f} GB",
                    "平台占用内存": f"{memory_info.rss / 1024 / 1024 / 1024:.2f} GB",
                    "占用比例": f"{virtual_memory.used / virtual_memory.total * 100:.2f}%"}
    return memory_total


def get_first_part_from_right(input_string, delimiter='-'):
    # 从右向左查找第一个分隔符的位置
    last_index = input_string.rfind(delimiter)

    if last_index != -1:
        # 使用切片操作获取第一个元素
        first_part = input_string[:last_index]
        return first_part
    else:
        # 如果没有找到分隔符，返回整个输入字符串
        return input_string


def count_element_in_list(lst, element_to_count):
    """
    统计列表中某一种元素出现的次数。

    参数:
    lst (list): 输入的列表。
    element_to_count: 要统计的元素。

    返回:
    int: 指定元素在列表中出现的次数。
    """
    count = lst.count(element_to_count)
    return count


if __name__ == '__main__':
    # # logs_path = os.path.join(BASE_DIR, "logs", "worker_logs")
    # # list_files(logs_path)
    #
    # # t = get_memory_usage()
    # # print(t)
    #
    # # 指定要扫描的路径
    # # target_path = os.path.join(BASE_DIR,'logs_back/worker_logs')
    # target_path = os.path.join('F:\\workSpace\\myGithub\\crawler-s-Gravestone\\backEnd\\logs/worker_logs')
    #
    # # 获取文件夹信息列表
    # folder_info_list = get_folder_sizes(target_path)
    #
    # # 打印文件夹信息
    # for folder_info in folder_info_list:
    #     print(f"Folder: {folder_info['folder_name']}")
    #     print(f"Size: {folder_info['size_human_readable']} ({folder_info['size_bytes']} bytes)")
    #     print(f"Size Ratio: {folder_info['size_ratio']:.2%}\n")

    temp = summarize_logs_by_wid("yesterday")[:10]
    print(temp)