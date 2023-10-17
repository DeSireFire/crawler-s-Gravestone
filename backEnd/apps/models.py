#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/10
# CreatTIME : 13:36
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import time
import datetime
from sqlalchemy.sql import func
from server_core.log import logger

from server_core.db import engine, Newsession


class Basejson():
    def json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 用户初始化，生成特殊用户
def inituser():
    from apps.users.models import Users
    session = Newsession()
    user = session.query(Users).filter_by(name='admin').first()
    if not user:
        adminuser = Users(
            name='admin', nicename="管理员",
            role='admin', password='123qwe',
            status='1'
        )
        session.add(adminuser)
        session.commit()
        session.flush()

    test_user = session.query(Users).filter_by(name='test').first()
    if not test_user:
        adminuser = Users(
            name='test', nicename="测试员",
            role='test', password='123456',
            status='1'
        )
        session.add(adminuser)
        session.commit()
        session.flush()

    from apps.projects.models import ProjectInfos
    # 创建一个测试项目
    project_demo = session.query(ProjectInfos).filter_by(name='项目测试demo').first()
    if not project_demo:
        project_demo = ProjectInfos(
            name='项目测试demo', author="admin",
            description="用于做开发测试和创建流程实践的项目。"
        )
        session.add(project_demo)
        session.commit()

    from apps.projects.models import WorkerInfos
    # 创建一个测试工作流
    workers_demo = session.query(WorkerInfos).filter_by(name='工作流定义测试demo').first()
    if not workers_demo:
        workers_demo = WorkerInfos(
            pid="3fec345932e98b8e37bfc167312c3953", crawl_frequency="临时",
            name='工作流定义测试demo',
            modify_user="admin",
            description="用于做开发测试和创建流程实践的工作流。"
        )
        session.add(workers_demo)
        session.commit()
        session.flush()

    from apps.projects.models import JobInfos
    # 创建一个测试任务实例
    # jobs_demo = session.query(JobInfos).filter_by(name='任务实例测试demo').first()
    jobs_demo = session.query(JobInfos).filter_by(wid='a158dc3a9d0f71283132f2c1127bc8c0').first()
    if not jobs_demo:
        jobs_demo = JobInfos(
            pid="3fec345932e98b8e37bfc167312c3953",
            wid="a158dc3a9d0f71283132f2c1127bc8c0",
            run_user="admin",
            log_file_path=r"F:\workSpace\myGithub\crawler-s-Gravestone\backEnd\logs\worker_logs\test_client_uper\2023-06-26_cxy_pubmed_2263_redis_luoben_rq.log",
        )
        session.add(jobs_demo)
        session.commit()
        session.flush()

    from apps.alarms.models import Alamers
    # 创建一个测试任务实例
    Alamers_demo = session.query(Alamers).filter_by().first()
    if not Alamers_demo:
        Alamers_demo = Alamers(
            name="测试用邮件告警器",
            email="xx@qq.com",
            desc="测试用占位用的邮箱告警器",
            resource="电子邮件"
        )
        Alamers_demo_qw = Alamers(
            name="测试用企微告警器",
            qw_token="kjbcsh893223f2525v426384624b6324b364hyt68j44654j644j64386j4626146fewgwr",
            desc="测试用占位用的企微告警器",
            resource="企微bot"
        )
        session.add(Alamers_demo)
        session.add(Alamers_demo_qw)
        session.commit()
        session.flush()

    from apps.alarms.models import AlamerJobs
    # 创建一个测试任务实例
    AlamerJobs_demo = session.query(AlamerJobs).filter_by().first()
    if not AlamerJobs_demo:
        AlamerJobs_demo = AlamerJobs(
            aid="418bacbe48b5ea11dcd8a17a11efddca",
            wid="a158dc3a9d0f71283132f2c1127bc8c0",
            name="测试邮箱告警任务",
            desc="测试用占位用的告警器",
            alarm_content="告警内容测试！",
            resource="电子邮件"
        )
        AlamerJobs_demo_qw = AlamerJobs(
            aid="418bacbe48b5ea11dcd8a17a11efddca",
            wid="327d52aece3b4a47de5dac899f3407e7",
            name="测试用企微告警任务",
            desc="测试用占位用的企微告警任务",
            alarm_content="告警内容测试！",
            resource="企微bot"
        )
        session.add(AlamerJobs_demo)
        session.add(AlamerJobs_demo_qw)
        session.commit()
        session.flush()

    from apps.programs.models import ProgramInfos
    # 创建一个测试任务实例
    Program_demo = session.query(ProgramInfos).first()
    if not Program_demo:
        Program_demo = ProgramInfos(
            name="测试程序1",
            git_repo="https://github.com/DeSireFire/hexo-circle-of-friends",
            requirements="requirements.txt",
            author="admin",
            description="这是一个用来测试的git程序",
        )
        Program_demo2 = ProgramInfos(
            name="测试程序爬虫2",
            git_repo="https://github.com/kong36088/BaiduImageSpider",
            requirements="requirements.txt",
            author="admin",
            description="这是一个用来测试的git程序",
        )
        session.add(Program_demo)
        session.add(Program_demo2)
        session.commit()
        session.flush()


def initdb():
    from . import db_Base
    # 导入各模块的模组，用于初始化
    from apps.users.models import Users
    from apps.workerLogs.models import worker_logs
    from apps.projects.models import ProjectInfos
    from apps.programs.models import ProgramInfos
    db_Base.metadata.create_all(engine)
    inituser()


if __name__ == '__main__':
    initdb()
