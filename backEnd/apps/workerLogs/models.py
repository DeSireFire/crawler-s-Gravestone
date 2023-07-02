#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/6/18
# CreatTIME : 11:40
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from apps import db_Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class worker_logs(db_Base):
    __tablename__ = 'worker_logs'
    id = Column(Integer, primary_key=True)
    log_id = Column(String(100), unique=True)
    name = Column(String(255))
    log_project = Column(String(50))
    remarks = Column(String(255))
    address = Column(String(255))
    create_time = Column(DateTime(), default=datetime.now())
    file_path = Column(String(255))

    def __init__(self, log_id, name, log_project, remarks, address, file_path):
        self.log_id = log_id
        self.name = name
        self.log_project = log_project
        self.remarks = remarks
        self.address = address
        self.file_path = file_path
