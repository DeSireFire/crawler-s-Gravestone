#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/6/25
# CreatTIME : 18:00
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'


from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
# 模型工具函数
from server_core.db import engine, Newsession

Base = declarative_base()

class CRUD:
    def __init__(self, model):
        """
        初始化CRUD类

        :param model: 一个继承了Base的模型
        """
        self.model = model
        self.db = Newsession()

    def create(self, obj_in):
        """
        创建一个新的对象

        :param obj_in: 一个Pydantic模型
        :return: 创建的对象
        """
        db_obj = self.model(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def read(self, **kwargs):
        """
        读取一个对象

        :param id_: 对象的id
        :return: 读取的对象
        """
        return self.db.query(self.model).filter_by(**kwargs).first()

    def update(self, obj_in):
        """
        更新一个对象

        :param obj_in: 一个Pydantic模型
        :return: 更新后的对象
        """
        db_obj = self.read(id=obj_in.id)
        for var, value in vars(obj_in).items():
            setattr(db_obj, var, value) if value else None
        self.db.commit()
        return db_obj

    def delete(self, id_):
        """
        删除一个对象

        :param id_: 对象的id
        """
        obj = self.read(id=id_)
        self.db.delete(obj)
        self.db.commit()

