#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/19
# CreatTIME : 11:01
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
# 初始化
import os

# 封装等级(低到高)
# auth、model <= views <= (users)init

# 导入视图
from .views import *

# 我需要你开发一个类，它主要的职责是通过wid字段检索任务监控表AlamerJobs：
# class AlamerJobs(db_Base, BaseJson):
#     """
#     id: number | undefined;
#     a_jid: string | undefined,
#     wid: string | undefined,
#     aid: string | undefined,
#     name: string | undefined,
#     resource: string | undefined,
#     desc: string | undefined,
#     alarm_content: string | undefined,
#     extra: string | undefined;
#     create_time: string | undefined;
#     """
#     __tablename__ = 'alamer_jobs'
#     id = Column(Integer, primary_key=True)
#     a_jid = Column(String(64), unique=True)
#     aid = Column(String(64), nullable=False)
#     wid = Column(String(64), nullable=False)
#     name = Column(String(255), nullable=False)
#     resource = Column(String(255), nullable=False)
#     desc = Column(String, nullable=True)
#     alarm_content = Column(String, nullable=True)
#     extra = Column(JSON, nullable=True)
#     create_time = Column(DateTime(), default=datetime.now(), server_default=func.now())
#
#     def __init__(self, aid=None, wid=None, a_jid=None, name=None,
#                  desc=None, extra=None, resource=None, alarm_content=None
#                  ):
#         self.aid = aid
#         self.wid = wid
#         self.a_jid = a_jid or get_md5(f"{resource}_{name}")
#         self.name = name
#         self.resource = resource
#         self.desc = desc
#         self.extra = extra
#         self.alarm_content = alarm_content
#
# class Alamers(db_Base, BaseJson):
#     """
#     id: number | undefined;
#     name: string | undefined,
#     email: string | undefined,
#     qw_token: string | undefined,
#     resource: string | undefined,
#     desc: string | undefined,
#     create_time: string | undefined;
#     update_time: string | undefined;
#     """
#     __tablename__ = 'alamers'
#     id = Column(Integer, primary_key=True)
#     aid = Column(String(64), unique=True)
#     name = Column(String(255), nullable=False)
#     email = Column(String(255), nullable=True)
#     qw_token = Column(String(255), nullable=True)
#     resource = Column(String(255), nullable=False)
#     desc = Column(String, nullable=True)
#     extra = Column(JSON, nullable=True)
#     create_time = Column(DateTime(), default=datetime.now(), server_default=func.now())
#
#     def __init__(self, aid=None, name=None, email=None, qw_token=None, desc=None, extra=None, resource=None):
#         self.aid = aid or get_md5(name)
#         self.name = name
#         self.email = email
#         self.qw_token = qw_token
#         self.resource = resource
#         self.desc = desc
#         self.extra = extra
# 当中是否有相同wid的数据。如果有，则获取到AlamerJobs中的有关所有数据，
# 遍历该数据，检测数据中aid，获取到告警器表（Alamers）当中aid相同的数据。
# 再判断Alamers数据中resource和AlamerJobs数据中的resource是否一致。
# 如果resource值一致，且值为"电子邮件"则调用之前开发的EmailSender类，
# 如果值为"企微BOT"则调用之前开发的WeChatMessenger类。


# 我需要你帮我开发一个程序，它会随着fastapi启动而跟着启动。
# 它主要的职责是，定期获取表中的监控任务表AlamerJobs中的wid字段，
# 去检索JobInfos
# 它会定期通过sqlalchemy获取该模组下的数据：
# class AlamerJobs(db_Base, BaseJson):
#     """
#     id: number | undefined;
#     a_jid: string | undefined,
#     wid: string | undefined,
#     aid: string | undefined,
#     name: string | undefined,
#     resource: string | undefined,
#     desc: string | undefined,
#     alarm_content: string | undefined,
#     extra: string | undefined;
#     create_time: string | undefined;
#     """
#     __tablename__ = 'alamer_jobs'
#     id = Column(Integer, primary_key=True)
#     a_jid = Column(String(64), unique=True)
#     aid = Column(String(64), nullable=False)
#     wid = Column(String(64), nullable=False)
#     name = Column(String(255), nullable=False)
#     resource = Column(String(255), nullable=False)
#     desc = Column(String, nullable=True)
#     alarm_content = Column(String, nullable=True)
#     extra = Column(JSON, nullable=True)
#     create_time = Column(DateTime(), default=datetime.now(), server_default=func.now())
#
#     def __init__(self, aid=None, wid=None, a_jid=None, name=None,
#                  desc=None, extra=None, resource=None, alarm_content=None
#                  ):
#         self.aid = aid
#         self.wid = wid
#         self.a_jid = a_jid or get_md5(f"{resource}_{name}")
#         self.name = name
#         self.resource = resource
#         self.desc = desc
#         self.extra = extra
#         self.alarm_content = alarm_content
# 拿到wid字段的数据去扫描另一个模组当中wid相同的所有数据：
# class JobInfos(db_Base, BaseJson):
#     __tablename__ = 'job_infos'
#     id = Column(Integer, primary_key=True)
#     wid = Column(String(64), nullable=False)
#     pid = Column(String(64), nullable=False)
#     jid = Column(String(64), nullable=False, unique=True)
#     p_nickname = Column(String(255))
#     w_nickname = Column(String(255))
#     name = Column(String(255), nullable=False, unique=True)
#     status = Column(Integer, default=0)   # 0 未知，1 执行中，2 结束， 3 中断， 4 失败
#     run_user = Column(String(255))
#     log_file_path = Column(Text)
#     log_lv_warning = Column(Integer, default=int(0))
#     log_lv_error = Column(Integer, default=int(0))
#     log_lv_info = Column(Integer, default=int(0))
#     log_lv_debug = Column(Integer, default=int(0))
#     items_count = Column(Integer, default=int(0))
#     extra = Column(JSON, nullable=True)
#     create_time = Column(DateTime(), default=datetime.now(), server_default=func.now())
#     end_time = Column(DateTime(), default=datetime.now(), onupdate=func.now())
#
#     def __init__(self, wid, pid=None, p_nickname=None, w_nickname=None, jid=None, run_user=None,  name=None,
#                  log_file_path=None, log_lv_warning=0, log_lv_error=0, log_lv_debug=0, log_lv_info=0, extra=None):
#         from apps.projects.components import get_fetch_one
#         dn = datetime.now()
#         now_time = dn.strftime('%Y-%m-%dT%H:%M:%S')
#         now_ts = int(dn.timestamp() * 1000)
#         w_info = get_fetch_one(model=WorkerInfos, wid=wid)
#         wname = w_info.get("name")
#         self.wid = wid
#         self.pid = pid
#         self.pid = self.pid if self.pid else w_info.get("pid")
#         self.p_nickname = p_nickname if p_nickname else get_fetch_one(model=ProjectInfos, pid=self.pid).get("name")
#         self.w_nickname = w_nickname if w_nickname else wname
#         self.jid = jid or get_md5(f"{wname}_{wid}_{now_time}")
#         self.name = name if name else f"{wname}-{now_ts}"
#         self.run_user = run_user
#         self.log_file_path = log_file_path
#         self.log_lv_warning = log_lv_warning
#         self.log_lv_error = log_lv_error
#         self.log_lv_info = log_lv_info
#         self.log_lv_debug = log_lv_debug
#         self.extra = extra
#         self.create_time = dn
#
#     def get_jid(self):
#         return self.jid
