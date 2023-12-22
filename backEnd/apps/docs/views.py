#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/25
# CreatTIME : 17:29
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from .components import get_query_all

"""
知识星球文档模块
"""
from .models import Docs
from pprint import pprint
from fastapi import requests
from server_core.log import logger
from .components import get_user_by_author, achmey_to_dict, get_query_docs, get_query_all, del_data_one
from server_core.db import engine, Newsession
from server_core.control import constructResponse
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends, status, Query

route = APIRouter()


@route.get("/get_my_docs", summary="获取个人文章列表")
async def get_my_docs(request: Request, author: str = Query(None)):
    """
    获取共享文章列表
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    content = {}
    _user = get_user_by_author(author) or None
    if not _user:
        callbackJson.statusCode = 500
        callbackJson.message = "未查询到该用户..."
        content["list"] = None
        content["pageTotal"] = 0
        return callbackJson.callBacker(content)

    if 'xxxadmin' in _user.role:
        res = get_query_all(Docs) or []
    else:
        res = get_query_docs(Docs, **{"author_id": _user.id}) or []

    # 转换为业务响应数据
    content["list"] = res or None
    content["pageTotal"] = len(res)
    return callbackJson.callBacker(content)


@route.get("/get_doc", summary="获取指定阅读文档")
async def get_doc(request: Request, doc_id: str = Query(None)):
    """
    获取指定阅读文档
    :return:
    """
    data = dict(request.query_params)
    doc_id = data.get("doc_id")     # 用于文章的查询
    reader = data.get("reader")     # 用于权限检查
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    doc_items = get_query_docs(Docs, **{"doc_id": doc_id}) or []
    doc_item = doc_items[0] if len(doc_items) >= 1 else None
    # todo 阅读者的权限检查
    content = {}
    # 转换为业务响应数据
    content["doc"] = doc_item
    return callbackJson.callBacker(content)


@route.get("/get_shape", summary="获取共享文章列表")
async def get_shape(request: Request):
    """
    获取共享文章列表
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    res = get_query_docs(Docs) or []
    content = {}
    # 转换为业务响应数据
    content["list"] = res
    print(f"get_shape:{content}")
    return callbackJson.callBacker(content)


@route.delete("/del_my_docs", summary="删除文章")
async def del_my_docs(request: Request, doc_id: str = Query(None), author: str = Query(None)):
    """
    删除文章
    参数以url传参的方式接收
    :param request: 请求对象
    :param doc_id: 文章id
    :param author: 操作者名称
    :return:
    """
    callbackJson = constructResponse()
    callbackJson.statusCode = 200
    del_data = dict(request.query_params)
    callbackJson.url = request.url
    session = Newsession()
    # 查询是否已存在相同的 doc_id
    doc_item = session.query(Docs).filter(Docs.doc_id == del_data['doc_id']).first() or None
    jugements = {
        "无效的id..": True if doc_item else False,
        "没有删除操作权限": True if doc_item and doc_item.author.name == del_data['author'] else False,
        "删除操作失败": del_data_one(model=Docs, **{'doc_id': del_data['doc_id']}),
    }
    content = {}
    if all(list(jugements.values())):
        callbackJson.message = f"{doc_id.title()} 删除成功..."
    else:
        callbackJson.statusCode = 404
        for k, v in jugements.items():
            if not v:
                callbackJson.message = k
    return callbackJson.callBacker(content)

@route.post("/update_doc", summary="新增文档")
async def update_doc(request: Request, docId: str = Query(None)):
    """
    通过传入工作流实例wid等信息创建实际的任务实例记录
    :param request:
    :param db: 数据库会话
    :param docId: 文档ID
    :return: 回调信息
    """
    fdata = await request.form()
    data = dict(fdata)
    callback_json = constructResponse()
    callback_json.statusCode = 400
    content = {}
    pprint(data)
    print(docId)

    session = Newsession()

    # 查询是否已存在相同的 doc_id
    existing_doc = session.query(Docs).filter(Docs.doc_id == docId).first()

    if existing_doc:
        # 如果已存在相同的 doc_id，则不保存并打印信息
        print(f"Document with doc_id {docId} already exists. Skipping save.")
    else:
        # # 如果docId为空，认为为新文章
        # if not data.get('docId'):

        # 如果不存在相同的 doc_id，则新增文档到数据库
        try:
            new_doc = Docs(**data)
            session.add(new_doc)
            session.commit()

            # 设置成功的回调信息
            callback_json.statusCode = 200
            content["docId"] = docId
        except Exception as e:
            print(f"Error saving document: {str(e)}")
            session.rollback()
        finally:
            session.close()

    return callback_json.callBacker(content)
