#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/10/9
# CreatTIME : 17:04
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import time
import datetime
import os
from sqlalchemy import func
from utils.other import get_md5
from server_core.log import logger
from datetime import datetime, timedelta
from server_core.db import engine, Newsession
from apscheduler.triggers.cron import CronTrigger
from apps.projects.models import JobInfos, WorkerInfos
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from apps.projects.models import ProjectInfos, WorkerInfos, JobInfos


"""
守护程序的子程序

定时任务
"""


# 定义一个示例函数，用于在定时任务中执行
def sample_job():
    print("这是一个定时任务的示例")


# 定期扫描过往任务实例,并对过期任务状态进行调整
def update_job_statuses():
    """
    扫描过往任务，对状态的修改
    # 0 未知，1 执行中，2 结束， 3 中断， 4 失败
    对除了结束和失败以外的所有任务，进行过期判断
    :return:
    """
    logger.info("update_job_statuses 启动。扫描过往任务实例,并对过期任务状态进行调整...")
    # 创建数据库连接
    session = Newsession()
    try:
        # 获取所有workInfos，生成字典
        work_infos = session.query(WorkerInfos).all()
        work_info_dict = {info.wid: info.crawl_frequency for info in work_infos}

        # 定义过期时间规则
        expiration_rules = {
            '日更': timedelta(days=1),
            '周更': timedelta(days=2),
            '月更': timedelta(days=7),
            '季更': timedelta(days=20),
            '年更': timedelta(days=30)
        }

        # 获取当前时间
        current_time = datetime.now()

        # 遍历工作流信息，处理任务状态
        updated_job_infos = []

        for wid, crawl_frequency in work_info_dict.items():
            expiration_period = expiration_rules.get(crawl_frequency)

            if expiration_period:
                expiration_time = current_time - expiration_period

                # 查询任务表中与当前工作流相关的任务
                jobs = session.query(JobInfos).filter(JobInfos.wid == wid, JobInfos.status.notin_([2, 4])).all()

                for job in jobs:
                    # 根据规则判断任务状态
                    if job.status == 0:
                        job.status = 4  # 未知转为失败
                    elif job.status == 1:
                        if job.log_lv_error or job.log_lv_info or job.log_lv_warning or job.items_count:
                            job.status = 3  # 执行中且有日志信息或数据项，状态转为中断
                        else:
                            job.status = 4  # 执行中且没有日志信息或数据项，状态转为失败
                    elif job.status == 3:
                        if job.log_lv_error or job.log_lv_info or job.log_lv_warning or job.items_count:
                            if job.end_time < expiration_time:
                                job.status = 2  # 中断且已过期，状态转为结束
                            else:
                                job.status = 3  # 中断且未过期，保持中断状态
                        else:
                            job.status = 4  # 中断且没有日志信息或数据项，状态转为失败

                    updated_job_infos.append(job)

        # 批量更新任务状态
        for job_info in updated_job_infos:
            session.add(job_info)

        # 提交事务
        session.commit()
    except Exception as e:
        logger.error(f"update_job_statuses 处理时发生了错误: {e}")
    finally:
        if session is not None:
            session.close()

# 使用示例
# update_job_statuses()
