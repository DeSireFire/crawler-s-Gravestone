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

from apps.projects import get_projects_info
from server_core.conf import BASE_DIR


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
    获取当前机器cpu占用率
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

    t = get_memory_usage()
    print(t)
