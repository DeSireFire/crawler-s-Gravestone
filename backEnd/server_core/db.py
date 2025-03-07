#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/10
# CreatTIME : 13:43
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import pymysql

import os

from sqlalchemy.exc import OperationalError

pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine, QueuePool
from .conf import BASE_DIR, conf, mysqlconf, pgdbconf, redisconf
from sqlalchemy.orm import sessionmaker
from utils.RedisDBHelper import RedisDBHelper

# 加载redis配置
if redisconf.host:
    rdb = RedisDBHelper(redisconf.db if redisconf.db else 0)
else:
    rdb = None

if conf.db == 'mysql':
    # 构建数据库连接字符串
    db_url = f"mysql://{mysqlconf.username}:{mysqlconf.password}@{mysqlconf.host}:{mysqlconf.port}/{mysqlconf.dbname}?charset=utf8mb4"

    # 创建数据库引擎
    engine = create_engine(
        db_url,                 # 数据库连接字符串
        echo=conf.debug,        # 是否输出SQL语句的调试信息
        pool_recycle=60 * 5,    # 连接池回收时间，避免连接过久
        pool_pre_ping=True,     # 启用连接池健康检查
        pool_size=10,           # max_connections = 500
        max_overflow=20         # 连接池允许的最大额外连接数
    )

elif conf.db == 'postgresql':
    engine = create_engine(
        f'postgresql+psycopg2://{pgdbconf.username}:{pgdbconf.password}@{pgdbconf.host}:{pgdbconf.port}/{pgdbconf.dbname}')
else:
    dbfile = os.path.join(BASE_DIR, 'DB.sqlite')
    # engine = create_engine(f'sqlite:///{dbfile}', echo=conf.debug, pool_recycle=60 * 5)
    engine = create_engine(f'sqlite:///{dbfile}', echo=conf.debug, pool_recycle=60 * 5,
                           poolclass=QueuePool, pool_size=10, max_overflow=20)


# DbSession = sessionmaker(bind=engine,autocommit=True)
# # DbSession = sessionmaker(bind=engine)
# session = DbSession()

# def Newsession():
#     DbSession = sessionmaker(bind=engine)
#     Session = DbSession()
#     return Session

def Newsession():
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            DbSession = sessionmaker(bind=engine)
            Session = DbSession()
            return Session
        except OperationalError as e:
            print(f"Database connection error: {e}. Retrying ({retries + 1}/{max_retries})...")
            retries += 1
    raise Exception("Failed to connect to the database after multiple attempts.")