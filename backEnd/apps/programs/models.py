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
from utils.other import get_md5
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text


class BaseJson:
    def json(self):
        tdict = self.__dict__
        if "_sa_instance_state" in tdict:
            del tdict["_sa_instance_state"]
        return tdict


class ProgramInfos(db_Base, BaseJson):
    """
    id: string | undefined;
    cid: string | undefined;
    name: string | undefined;
    git_repo: string | undefined;
    repo_path: string | undefined;
    requirements: string | undefined;
    interpreter: string | undefined;
    description: string | undefined;
    author: string | undefined;
    create_time: string | undefined;
    update_time: string | undefined;
    """
    __tablename__ = 'program_infos'
    id = Column(Integer, primary_key=True)
    cid = Column(String(64), unique=True)
    name = Column(String(255), nullable=False)
    git_repo = Column(String(255), nullable=True)
    repo_path = Column(Text)
    base_path = Column(Text)
    shell = Column(Text)
    requirements = Column(String(255), nullable=True)
    interpreter = Column(String(255), nullable=True)
    author = Column(String, nullable=True)
    description = Column(String, nullable=True)
    extra = Column(JSON, nullable=True)
    create_time = Column(DateTime(), default=datetime.now)
    update_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __init__(self,
                 cid=None, name=None, git_repo=None, repo_path=None, author=None,
                 requirements=None, interpreter=None, description=None, extra=None,
                 ):
        self.cid = cid or get_md5(name)
        self.name = name
        self.git_repo = git_repo
        self.repo_path = repo_path
        self.requirements = requirements
        self.interpreter = interpreter
        self.author = author
        self.description = description
        self.extra = extra

__all__ = [
    "ProgramInfos",
]
