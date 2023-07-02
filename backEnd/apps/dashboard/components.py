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
from server_core.conf import BASE_DIR


def list_files(path):
    count = 0
    for root, dirs, files in os.walk(path):
        # print(f"info =======> {os.path.join(root)}")
        # print(f"files =======> {files}")
        for file in files:
            if file.endswith('.log'):
                print(f"info =======> {os.path.join(root, file)}")
                count += 1
    print(f"count =======> {count}")
    return count

def get_machine_memory_usage_percent():
    """
    获取当前机器cpu占用率
    :return:
    """
    return int(psutil.virtual_memory()._asdict().get('percent'))

if __name__ == '__main__':
    logs_path = os.path.join(BASE_DIR, "logs", "worker_logs")
    list_files(logs_path)
