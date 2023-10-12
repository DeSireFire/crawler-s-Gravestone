#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/27
# CreatTIME : 14:03
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from server_core.guardApi import TaskScheduler
from server_core.guardWare import *
from server_core.conf import conf, LogLevel
from server_core.hello import logger

if __name__ == '__main__':

    task_scheduler = TaskScheduler()
    # 添加任务
    # task_scheduler.add_task("task1", sample_job, "interval", seconds=10)
    # 过往任务过期判断
    task_scheduler.add_task("update_job_statuses", update_job_statuses, "interval", seconds=600)
    # 系统表auto_increment重置
    task_scheduler.add_task("base_auto_increment", base_auto_increment, "cron", hour=0, minute=0)

    try:
        # 这里可以添加你的其他程序逻辑
        # 例如，可以运行一个无限循环以保持程序运行，或者在这里执行其他任务
        while True:
            print("平台守护程序运行中..")
            time.sleep(600)
    except (KeyboardInterrupt, SystemExit):
        # 当你手动停止程序时，由atexit注册的退出处理函数会关闭定时任务调度器
        pass

    # 清理所有任务
    print("清理所有任务...")
    task_scheduler.clear_all_tasks()

    # # with 代码块来降低意外崩溃时，子程没正常关闭的情况
    # with TaskScheduler() as task_scheduler:
    #     # 添加任务
    #     # task_scheduler.add_task("task1", sample_job, "interval", seconds=10)
    #     # 任务状态判断
    #     task_scheduler.add_task("update_job_statuses", update_job_statuses, "interval", seconds=600)
    #     # 系统表auto_increment重置
    #     task_scheduler.add_task("base_auto_increment", base_auto_increment, "cron", hour=17, minute=34)
    #
    #     try:
    #         # 这里可以添加你的其他程序逻辑
    #         # 例如，可以运行一个无限循环以保持程序运行，或者在这里执行其他任务
    #         while True:
    #             print("平台守护程序运行中..")
    #             time.sleep(600)
    #     except (KeyboardInterrupt, SystemExit):
    #         # 当你手动停止程序时，由atexit注册的退出处理函数会关闭定时任务调度器
    #         pass
    #
    #     # 清理所有任务
    #     # print("清理所有任务...")
    #     # task_scheduler.clear_all_tasks()



