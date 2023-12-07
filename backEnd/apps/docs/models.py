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
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from apps.docs.components import generate_unique_id, get_user_by_author
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text


class BaseJson:
    def json(self):
        tdict = self.__dict__
        if "_sa_instance_state" in tdict:
            del tdict["_sa_instance_state"]
        return tdict


class Docs(db_Base, BaseJson):
    """
    表示文档的数据库模型。

    id: 文档的唯一标识号，自增长。
    doc_id: 文档的ID，唯一标识。
    title: 文档标题。
    author: 文档作者。
    content: 文档内容。
    md_content: Markdown格式的文档内容。
    desc: 文档描述。
    extra: 额外的文档信息，以JSON格式存储。
    create_time: 文档创建时间，默认为当前时间。
    """

    __tablename__ = 'Docs'
    id = Column(Integer, primary_key=True)
    doc_id = Column(String(64), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    # author_id = Column(String(255), nullable=True)
    # author = Column(String(255), nullable=True)
    author_id = Column(Integer, ForeignKey('users.id'))  # 设置为 users 表的外键
    reading_permissions = Column(String(64), nullable=False, default='全公开')  # 阅读权限：'仅自己', '全公开', '指定人'
    article_source = Column(String(64), nullable=False, default='原创')  # 文章来源：原创，转载
    content = Column(Text, nullable=True)  # 修改为 Text 类型
    md_content = Column(Text, nullable=True)  # 修改为 Text 类型
    desc = Column(Text, nullable=True)
    extra = Column(JSON, nullable=True)
    create_time = Column(DateTime(), default=datetime.now(), server_default=func.now())
    update_time = Column(DateTime(timezone=True), default=datetime.now(), onupdate=func.now())

    # 关联关系
    author = relationship('Users', backref='documents')  # 创建与Users模组的关系

    def __init__(self, doc_id=None, title=None, author=None, content=None, desc=None, md_content=None, extra=None):
        """
        初始化文档对象。

        Parameters:
        - title: 文档标题。
        - author: 文档作者。
        - content: 文档内容。
        - md_content: Markdown格式的文档内容。
        - desc: 文档描述。
        - extra: 额外的文档信息，以JSON格式存储。
        """
        self.doc_id = generate_unique_id(title) if not doc_id else doc_id
        self.title = title
        # self.author = author
        self.desc = desc
        self.content = content
        self.md_content = md_content
        if not desc and md_content:
            self.desc = f"{md_content[:60]}..."
        # todo 当前根据前端的用户民来查询用户id然后才入库
        # todo 后期最好通过前端在登录时就在客户端登记用户id
        user = get_user_by_author(author_name=author)
        if author and user:
            self.author_id = user.id
        self.extra = extra


# 关联表
class DocPermissions(db_Base):
    __tablename__ = 'doc_permissions'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, ForeignKey('Docs.id'))
    author_id = Column(Integer, ForeignKey('users.id'))  # 设置为 users 表的外键

    # 创建关系
    doc = relationship('Docs', backref=backref('permissions', cascade='all, delete-orphan'))
    user = relationship('Users', backref='accessible_docs')

    def __init__(self, doc_id=None, user_id=None):
        self.doc_id = doc_id
        self.user_id = user_id

__all__ = [
    "Docs",
    "DocPermissions",
]
