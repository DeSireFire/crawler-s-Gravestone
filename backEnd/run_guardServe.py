#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/27
# CreatTIME : 14:03
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import time
from server_core.hello import logger
from server_core.conf import conf, LogLevel
from server_core.guardApi import TaskScheduler
from guard_server.guardWare import update_job_statuses, base_auto_increment, clean_status_for_all_old_jobs, \
    update_logs_file, sample_job, update_logging

if __name__ == '__main__':

    # task_scheduler = TaskScheduler()
    # # # 添加任务
    # # task_scheduler.add_task("测试任务", sample_job, "interval", seconds=1)
    # # 按频率对任务过期状态处理
    # task_scheduler.add_task("update_job_statuses", update_job_statuses, "interval", seconds=600)
    # # 系统表auto_increment重置
    # task_scheduler.add_task("base_auto_increment", base_auto_increment,
    #                         "cron", hour="23", minute="30")
    # # 最后更新时间超时任务的状态处理
    # task_scheduler.add_task("clean_status_for_all_old_jobs", clean_status_for_all_old_jobs, "cron", hour=0, minute=0)
    # # 定时将日志缓存，保存到日志文本
    # task_scheduler.add_task("update_logs_file", update_logs_file,
    #                         "cron", hour="0-23", minute=",".join([str(x) for x in range(0, 60, 3)]))
    #
    # # 启动调度器
    # task_scheduler.start_scheduler()
    #
    # # S属性大爆发，sleeping,秒
    # step_time = 60
    # try:
    #     # 常驻执行的其他程序
    #     # 例如，可以运行一个无限循环以保持程序运行，或者在这里执行其他任务
    #     while True:
    #         update_logging(rkey="crawl_monitor:RawLogList")
    #         logger.info(f"常驻任务，周期执行结束..睡眠{step_time}秒")
    #         time.sleep(step_time)
    # except (KeyboardInterrupt, SystemExit):
    #     # 当你手动停止程序时，由atexit注册的退出处理函数会关闭定时任务调度器
    #     print("守护程序终止..")
    #     pass
    #
    # # 清理所有任务
    # print("清理所有任务...")
    # task_scheduler.clear_all_tasks()

    # with 代码块来降低意外崩溃时，子程没正常关闭的情况
    with TaskScheduler() as task_scheduler:
        # # 添加任务
        # task_scheduler.add_task("测试任务", sample_job, "interval", seconds=1)
        # 按频率对任务过期状态处理
        task_scheduler.add_task("update_job_statuses", update_job_statuses, "interval", seconds=600)
        # 系统表auto_increment重置
        task_scheduler.add_task("base_auto_increment", base_auto_increment,
                                "cron", hour="23", minute="30")
        # 最后更新时间超时任务的状态处理
        task_scheduler.add_task("clean_status_for_all_old_jobs", clean_status_for_all_old_jobs, "cron", hour=0,
                                minute=0)
        # 定时将日志缓存，保存到日志文本
        task_scheduler.add_task("update_logs_file", update_logs_file,
                                "cron", hour="0-23", minute=",".join([str(x) for x in range(0, 60, 3)]))

        # 启动调度器
        task_scheduler.start_scheduler()

        # S属性大爆发，sleeping,秒
        step_time = 60
        try:
            # 常驻执行的其他程序
            # 例如，可以运行一个无限循环以保持程序运行，或者在这里执行其他任务
            while True:
                update_logging(rkey="crawl_monitor:RawLogList")
                logger.info(f"常驻任务，周期执行结束..睡眠{step_time}秒")
                time.sleep(step_time)
        except (KeyboardInterrupt, SystemExit):
            # 当你手动停止程序时，由atexit注册的退出处理函数会关闭定时任务调度器
            print("守护程序终止..")
            pass

        # 清理所有任务
        # print("清理所有任务...")
        # task_scheduler.clear_all_tasks()
