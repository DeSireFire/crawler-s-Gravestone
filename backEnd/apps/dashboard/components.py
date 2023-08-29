#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/6/27
# CreatTIME : 23:20 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import os
import psutil
from datetime import datetime, timedelta
from apps.programs import get_query_all
from apps.projects import get_projects_info
from apps.programs.models import ProgramInfos
from apps.projects.models import JobInfos
from server_core.conf import BASE_DIR
from server_core.db import engine, Newsession


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


def get_projects_count():
    """
    获取项目数量
    :return:
    """
    pro_list = get_projects_info() or []
    names = [d["name"] for d in pro_list if d["name"]]
    return len(names)


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


if __name__ == '__main__':
    # logs_path = os.path.join(BASE_DIR, "logs", "worker_logs")
    # list_files(logs_path)

    # t = get_memory_usage()
    # print(t)

    # 指定要扫描的路径
    # target_path = os.path.join(BASE_DIR,'logs_back/worker_logs')
    target_path = os.path.join('F:\\workSpace\\myGithub\\crawler-s-Gravestone\\backEnd\\logs/worker_logs')

    # 获取文件夹信息列表
    folder_info_list = get_folder_sizes(target_path)

    # 打印文件夹信息
    for folder_info in folder_info_list:
        print(f"Folder: {folder_info['folder_name']}")
        print(f"Size: {folder_info['size_human_readable']} ({folder_info['size_bytes']} bytes)")
        print(f"Size Ratio: {folder_info['size_ratio']:.2%}\n")