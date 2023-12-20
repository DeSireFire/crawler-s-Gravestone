#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/10/9
# CreatTIME : 17:04
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import os
import time
import datetime
from server_core.db import rdb
from utils.other import get_md5
from server_core.log import logger
from guard_server.components import *
from datetime import datetime, timedelta
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

    # 使用示例
    # update_job_statuses()

    :return:
    """
    logger.info("update_job_statuses 启动。扫描过往任务实例,并对过期任务状态进行调整...")
    # todo 待优化
    # 创建数据库连接
    session = Newsession()
    try:
        # 获取所有workInfos，生成采集频率字典
        work_infos = get_workers_all()
        work_info_dict = {info["wid"]: info["crawl_frequency"] for info in work_infos}

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
                jobs = get_jobs_for_update_job_statuses(wid=wid) or []

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


# 对平台各表id起始数重置
def base_auto_increment():
    tables = [
        "worker_infos",
        "project_infos",
        "alamer_jobs",
        "alamers",
        "users",
    ]
    try:
        for t in tables:
            reset_auto_increment_table(t)
    except Exception as e:
        logger.error(f"守护任务发生错误，base_auto_increment 错误信息:{e}")


# 批量更新日志到log文本
def update_logs_file():
    """
    获取保存在redis中缓存的日志信息
    :return:
    """
    logger.info("update_logs_file 启动。批量更新日志到log文本...")
    rkeys = get_redis_keys("crawl_monitor:logging:*")

    for rk in rkeys:
        # 遍历key名称，裁剪crawl_monitor:logging:[jid]:[lv]来获取jid
        parts = rk.split(":")
        jid = parts[2] if len(parts) >= 3 else None
        log_level = parts[3] if len(parts) >= 4 else None

        # 如果jid为空，认为该key不符合约定，跳过
        if not jid:
            continue

        # 通过sqlalchemy获取mysql上指定jid相符的数据，返回值是一个字典
        job_data = get_job_by_jid(jid=jid)
        log_file_path = job_data["log_file_path"]

        # 创建目录or目录检查
        log_directory = os.path.dirname(log_file_path)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        else:
            logger.info(f"目录已存在:{log_directory}")

        # 通过redis的key名称，弹出列表中的数据
        # log_records = batch_pop_from_redis_list(rk, 10) or [] # 调试时，但是后进后出
        log_records = batch_pop_from_redis_list_fifo(rk) or []  # 调试时，先进先出，时间升序
        # log_records = pop_all_from_redis_list_transaction(rk) or []  # 并发大时，使用watch事务监控,处理期间列表发生变化则处理失败，重新开始

        if log_records:
            # 总日志
            if not log_level:
                logger.info(f"任务:{jid} 日志写入 {log_file_path}..")
                with open(log_file_path, "a+", encoding="utf-8", ) as main_log:
                    main_log.write('\n'.join(log_records) + '\n')

            # 等级分流日志
            if log_level:
                sub_path = rename_log_file(log_file_path, log_level)
                logger.info(f"任务:{jid} 日志写入 {sub_path}..")
                with open(sub_path, "a+", encoding="utf-8", ) as sub_log:
                    sub_log.write('\n'.join(log_records) + '\n')


# 检测所有任务
def clean_status_for_all_old_jobs():
    """
    筛选所有过期任务
    最后更新时间超过7天的任务一律失败处理
    :return:
    """
    logger.info("clean_status_for_all_old_jobs 启动。最后更新时间超过7天的任务一律失败处理...")
    session = Newsession()
    try:
        # 计算昨天的日期
        lastweek = datetime.now() - timedelta(days=7)

        # 查询指定wid下昨天和昨天以前的数据，status为0或1

        old_jobs = session.query(JobInfos) \
            .filter(JobInfos.end_time <= lastweek) \
            .filter(JobInfos.status.in_([0, 1, 3])) \
            .all()

        # 更新这些数据的status
        # 0 未知，1 执行中，2 结束， 3 中断， 4 错误
        # 状态未知 改为 中断
        # 状态执行中 改为 结束
        for job in old_jobs:
            job.status = 4

        # 提交更改
        session.commit()
        logger.info(f"成功更新 {len(old_jobs)} 条数据的 status 为 2")
    except Exception as e:
        session.rollback()  # 回滚事务以防出现错误
        logger.error(f"update_status_to_2_for_old_jobs 发生错误：{e}")
    finally:
        session.close()


# 日志服务处理移植
def update_logging(rkey: str = "crawl_monitor:RawLogList"):
    """
    接收客户端日志
    {'args': '()',
     'created': '1690426537.0822754',
     'exc_info': 'None',
     'exc_text': 'None',
     'extra': '{"ip": "192.168.9.193", "log_name": "单例爬虫测试日志", "project_name": '
              '"高德地图", "token": "a158dc3a9d0f71283132f2c1127bc8c0"}',
     'filename': 'logClient.py',
     'funcName': '<module>',
     'levelname': 'DEBUG',
     'levelno': '10',
     'lineno': '112',
     'module': 'logClient',
     'msecs': '82.275390625',
     'msg': '这是一条 调试 日志，发出来测试一下！！！ cpu占用：57%',
     'name': '单例爬虫测试日志',
     'pathname': 'F:\\workSpace\\myGithub\\crawler-s-Gravestone\\backEnd\\log_server\\logClient.py',
     'process': '15080',
     'processName': 'MainProcess',
     'relativeCreated': '146.44455909729004',
     'stack_info': 'None',
     'thread': '1028',
     'threadName': 'MainThread'}
    {'ip': '192.168.9.193',
     'log_name': '单例爬虫测试日志',
     'project_name': '高德地图',
     'token': 'a158dc3a9d0f71283132f2c1127bc8c0'}

    :param request:
    :return:
    """
    callback = None
    while rdb.server.exists(rkey):
        logger.info("检测到日志流缓存数据...")
        # 获取日志流传送的信息
        log_data = json.loads(rdb.server.rpop(rkey)) if rdb.server.exists(rkey) else {}
        if not log_data:
            callback = None

        # 日志附加信息
        extra_data = json.loads(log_data.get("extra"))
        # 工作流密钥
        jid = extra_data.get("jid")
        # 预留备用信息传递
        meta = extra_data.get("meta")
        wid = extra_data.get("token")
        # 同步到数据库
        try:

            # 获取工作流信息=>
            # 生成任务实例的jid=>
            # 通过jid获取任务实例信息，如果没有就生成新的任务实例=>

            # 同步监控数据到数据库
            job_info = get_fetch_one(JobInfos, jid=jid)
            # 检测任务是否存在
            if not job_info:
                err = f"{jid} 未查询到该任务实例。日志信息明细：{log_data}。 可能是任务被删除。"
                logger.error(err)
                alarm_handler = AlarmHandler()

                asyncio.run(
                    alarm_handler.handle_alarm(
                        wid,
                        f'任务名称: {job_info["name"]}\n',
                        f'告警信息: {log_data["msg"]}\n',
                    ))
                callback = False

            # 状态
            job_info = handleStatus(job_info, log_data)

            # 入库数据计数
            job_info = handleItemsCount(job_info, log_data)

            # 日志内容缓存&日志等级统计
            job_info = handleLevelTotal(job_info, log_data)

            # 保存更新数据
            job_info_new = update_data(JobInfos, [job_info])

            # 获取日志文件路径
            # 已经交给守护程序处理
            # await handleLogTextSave(job_info, log_data)

            # 告警任务推送
            handleAlarm(job_info, log_data)

            logger.info(f"{jid} 本批次日志流缓存处理结束！")
            callback = True

        except Exception as err:
            logger.error(f"{jid} 日志流缓存处理错误！错误原因：{err}")
            callback = False

    logger.info(f"没有需要处理的日志流...")
    return callback


if __name__ == '__main__':
    update_logs_file()
