#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/18
# CreatTIME : 16:54
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import json
from server_core.db import rdb
import datetime

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        from datetime import date, datetime
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def create_access_token(data: dict) -> str:
    name = data.get("name")
    encoded_jwt = f"nimadeWhy_{name}_temp_fake"
    rkey = f"bearer:{encoded_jwt}"
    rdb.set(rkey, json.dumps(data, cls=ComplexEncoder, ensure_ascii=True))
    # 一周过期
    rdb.server.expire(rkey, datetime.timedelta(weeks=1))
    return encoded_jwt
