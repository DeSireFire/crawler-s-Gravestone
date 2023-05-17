#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/10
# CreatTIME : 13:43
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import pymysql

pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
import os
from .conf import BASE_DIR, conf, mysqlconf, pgdbconf, redisconf
from sqlalchemy.orm import sessionmaker
from utils.RedisDBHelper import RedisDBHelper

# 加载redis配置
if redisconf.host:
    rdb = RedisDBHelper(redisconf.db if redisconf.db else 0)

if conf.db == 'mysql':
    engine = create_engine(
        f"mysql://{mysqlconf.username}:{mysqlconf.password}@{mysqlconf.host}:{mysqlconf.port}/{mysqlconf.dbname}?charset=utf8",
        echo=conf.debug, pool_recycle=60 * 5)
elif conf.db == 'postgresql':
    engine = create_engine(
        f'postgresql+psycopg2://{pgdbconf.username}:{pgdbconf.password}@{pgdbconf.host}:{pgdbconf.port}/{pgdbconf.dbname}')
else:
    dbfile = os.path.join(BASE_DIR, 'DB.sqlite')
    engine = create_engine(f'sqlite:///{dbfile}', echo=conf.debug, pool_recycle=60 * 5)


# DbSession = sessionmaker(bind=engine,autocommit=True)
# # DbSession = sessionmaker(bind=engine)
# session = DbSession()

def Newsession():
    DbSession = sessionmaker(bind=engine)
    Session = DbSession()
    return Session
