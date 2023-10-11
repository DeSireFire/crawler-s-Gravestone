#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/10/9
# CreatTIME : 17:04
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import time
import atexit
import datetime
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

"""
守护程序

用于定期检查各模块数据状态，
脱离网络请求，独立处理各项业务的程序
"""


# 定义一个示例函数，用于在定时任务中执行
def sample_job():
    print("这是一个定时任务的示例")


class TaskScheduler:
    def __init__(self):
        # 创建一个定时任务调度器
        self.scheduler = BackgroundScheduler()

        # 注册退出处理函数，确保在程序退出时关闭调度器
        atexit.register(self.stop_scheduler)

    def __enter__(self):
        """
        元函数
        启动调度器，开始执行任务
        """
        self.scheduler.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        元函数
        停止调度器，停止执行任务
        """
        self.scheduler.shutdown()

    def add_task(self, task_id, func, trigger_type, **trigger_args):
        """
        添加任务到调度器

        参数:
            - task_id (str): 任务的唯一标识符
            - func (callable): 要执行的函数
            - trigger_type (str): 触发器类型，可以是 "interval" 或 "cron"
            - **trigger_args: 触发器的参数，根据触发器类型而变化
        """
        if trigger_type == "interval":
            trigger = IntervalTrigger(**trigger_args)
        elif trigger_type == "cron":
            trigger = CronTrigger(**trigger_args)
        else:
            raise ValueError("不支持的触发器类型")

        self.scheduler.add_job(func, trigger=trigger, id=task_id)

    def remove_task(self, task_id):
        """
        从调度器中移除任务

        参数:
            - task_id (str): 要移除的任务的唯一标识符
        """
        self.scheduler.remove_job(task_id)

    def clear_all_tasks(self):
        """
        清理所有调度任务
        """
        self.scheduler.remove_all_jobs()

    def modify_task(self, task_id, trigger_type, **trigger_args):
        """
        修改任务的触发器

        参数:
            - task_id (str): 要修改的任务的唯一标识符
            - trigger_type (str): 新触发器类型，可以是 "interval" 或 "cron"
            - **trigger_args: 新触发器的参数，根据触发器类型而变化
        """
        if trigger_type == "interval":
            trigger = IntervalTrigger(**trigger_args)
        elif trigger_type == "cron":
            trigger = CronTrigger(**trigger_args)
        else:
            raise ValueError("不支持的触发器类型")

        self.scheduler.reschedule_job(task_id, trigger=trigger)

    def get_all_tasks(self) -> list:
        """
        获取所有任务的列表

        返回:
            - List[dict]: 包含任务信息的字典列表
        """
        jobs = self.scheduler.get_jobs()
        task_list = []
        for job in jobs:
            trigger_type = job.trigger.__class__.__name__
            trigger_args = {}
            if trigger_type == "IntervalTrigger":
                trigger_args = {
                    "seconds": job.trigger.interval.seconds
                }
            elif trigger_type == "CronTrigger":
                trigger_args = {
                    "year": job.trigger.fields[0].get_value(datetime.datetime.now()),
                    "month": job.trigger.fields[1].get_value(datetime.datetime.now()),
                    "day": job.trigger.fields[2].get_value(datetime.datetime.now()),
                    "hour": job.trigger.fields[3].get_value(datetime.datetime.now()),
                    "minute": job.trigger.fields[4].get_value(datetime.datetime.now()),
                    "second": job.trigger.fields[5].get_value(datetime.datetime.now()),
                }

            task_info = {
                "id": job.id,
                "next_run_time": job.next_run_time,
                "trigger_type": trigger_type,
                "trigger_args": trigger_args,
            }
            task_list.append(task_info)
        return task_list

    def start_scheduler(self):
        """
        启动调度器，开始执行任务
        """
        self.scheduler.start()

    def stop_scheduler(self):
        """
        停止调度器，释放资源
        """
        if self.scheduler:
            self.scheduler.shutdown()


# 示例用法
if __name__ == "__main__":
    task_scheduler = TaskScheduler()

    # 添加任务
    # task_scheduler.add_task("task1", lambda: print("任务1执行了"), "interval", seconds=10)
    task_scheduler.add_task("task1", sample_job, "interval", seconds=10)

    # 启动调度器
    task_scheduler.start_scheduler()

    # 获取所有任务
    tasks = task_scheduler.get_all_tasks()
    print("所有任务:")
    for task in tasks:
        print(task)

    time.sleep(30)

    # 修改任务的触发器
    task_scheduler.modify_task("task1", "cron", hour=0, minute=30)

    # 获取修改后的任务列表
    tasks = task_scheduler.get_all_tasks()
    print("\n修改后的任务:")
    for task in tasks:
        print(task)

    # 移除任务
    task_scheduler.remove_task("task1")

    # 停止调度器
    task_scheduler.stop_scheduler()
