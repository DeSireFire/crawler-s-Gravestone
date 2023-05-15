#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/4/11
# CreatTIME : 14:00
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import copy
import json
import logging
import time
from pprint import pprint
from urllib.parse import parse_qs

from fastapi import FastAPI, Request, status
import random
import uvicorn
import requests
from pydantic.main import BaseModel
from redis import Redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list


@app.on_event("startup")
async def startup_event():
    setattr(app.state, "redis", Redis(host="192.168.60.122", port=6380, db=10, decode_responses=True))


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/table.test")
async def read_root():
    temp = {
        "list": [{
            "id": 1,
            "name": "张三",
            "money": 123,
            "address": "广东省东莞市长安镇",
            "state": "成功",
            "date": "2019-11-1",
            "thumb": "https://lin-xin.gitee.io/images/post/wms.png"
        },
            {
                "id": 2,
                "name": "李四",
                "money": 456,
                "address": "广东省广州市白云区",
                "state": "成功",
                "date": "2019-10-11",
                "thumb": "https://lin-xin.gitee.io/images/post/node3.png"
            },
            {
                "id": 3,
                "name": "王五",
                "money": 789,
                "address": "湖南省长沙市",
                "state": "失败",
                "date": "2019-11-11",
                "thumb": "https://lin-xin.gitee.io/images/post/parcel.png"
            },
            {
                "id": 4,
                "name": "赵六",
                "money": 1011,
                "address": "福建省厦门市鼓浪屿",
                "state": "成功",
                "date": "2019-10-20",
                "thumb": "https://lin-xin.gitee.io/images/post/notice.png"
            },
        ],
        "pageTotal": 4
    }
    return temp


@app.get("/rset")
async def read_root():
    temp = {
        "list": [
            {
                "id": 1,
                "name": "张三",
                "money": 123,
                "address": "广东省东莞市长安镇",
                "state": "成功",
                "date": "2019-11-1",
                "thumb": "https://lin-xin.gitee.io/images/post/wms.png"
            },
            {
                "id": 2,
                "name": "李四",
                "money": 456,
                "address": "广东省广州市白云区",
                "state": "成功",
                "date": "2019-10-11",
                "thumb": "https://lin-xin.gitee.io/images/post/node3.png"
            },
            {
                "id": 3,
                "name": "王五",
                "money": 789,
                "address": "湖南省长沙市",
                "state": "失败",
                "date": "2019-11-11",
                "thumb": "https://lin-xin.gitee.io/images/post/parcel.png"
            },
            {
                "id": 4,
                "name": "赵六",
                "money": 1011,
                "address": "福建省厦门市鼓浪屿",
                "state": "成功",
                "date": "2019-10-20",
                "thumb": "https://lin-xin.gitee.io/images/post/notice.png"
            },
        ],
        "pageTotal": 4
    }
    rdb = app.state.redis
    rs = rdb.smembers("main_amap:keywords_poi:ERROR")
    rs = list(rs)
    t = []
    for i in rs:
        ii = json.loads(i)
        t.append({
            "id": ii.get("keyword_id"),
            "name": i,
        })
    temp["list"] = t
    return temp


@app.get("/rechart")
async def rec():
    rjson = {
        "title": {
            "text": "数据统计 有点厉害",
        },
        "tooltip": {
            "trigger": "axis",
        },
        "legend": {
            "x": 'center',
            "y": 'bottom',
            "data": ["Email", "Union Ads", "Video Ads", "Direct", "Search Engine"],
        },
        "grid": {
            # "left": "3%",
            # "right": "4%",
            # "bottom": "3%",
            "containLabel": True,
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {},
            },
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {
            "type": "value",
        },
        "series": [
            {
                "name": "Email",
                "type": "line",
                "stack": "Total",
                "data": [120, 132, 101, 134, 90, 230, 210],
            },
            {
                "name": "Union Ads",
                "type": "line",
                "stack": "Total",
                "data": [220, 182, 191, 234, 290, 330, 310],
            },
            {
                "name": "Video Ads",
                "type": "line",
                "stack": "Total",
                "data": [150, 232, 201, 154, 190, 330, 410],
            },
            {
                "name": "Direct",
                "type": "line",
                "stack": "Total",
                "data": [320, 332, 301, 334, 390, 330, 320],
            },
            {
                "name": "Search Engine",
                "type": "line",
                "stack": "Total",
                "data": [820, 932, 901, 934, 1290, 1330, 1320],
            },
        ],
    }
    return rjson


@app.get("/recharts")
async def recs():
    rjson = {
        "title": {
            "text": "数据统计 有点厉害",
        },
        "tooltip": {
            "trigger": "axis",
        },
        "legend": {
            "x": 'center',
            "y": 'bottom',
            "data": ["Email", "Union Ads", "Video Ads", "Direct", "Search Engine"],
        },
        "grid": {
            # "left": "3%",
            # "right": "4%",
            # "bottom": "3%",
            "containLabel": True,
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {},
            },
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {
            "type": "value",
        },
        "series": [
            {
                "name": "Email",
                "type": "line",
                "stack": "Total",
                "data": [120, 132, 101, 134, 90, 230, 210],
            },
            {
                "name": "Union Ads",
                "type": "line",
                "stack": "Total",
                "data": [220, 182, 191, 234, 290, 330, 310],
            },
            {
                "name": "Video Ads",
                "type": "line",
                "stack": "Total",
                "data": [150, 232, 201, 154, 190, 330, 410],
            },
            {
                "name": "Direct",
                "type": "line",
                "stack": "Total",
                "data": [320, 332, 301, 334, 390, 330, 320],
            },
            {
                "name": "Search Engine",
                "type": "line",
                "stack": "Total",
                "data": [820, 932, 901, 934, 1290, 1330, 1320],
            },
        ],
    }
    rjsons = []
    for i in range(1, random.randint(2, 5)):
        t = copy.deepcopy(rjson)
        t["title"]["text"] = f"数据统计({i})"
        for s in t["series"]:
            s["data"] = random_int_list(100, 999, 7)
        rjsons.append(t)
    return rjsons


@app.get("/rschart")
async def rc():
    cookies = {
        'order': 'id%20desc',
        'serverType': 'nginx',
        'pro_end': '-1',
        'ltd_end': '-1',
        'memSize': '3931',
        'bt_user_info': '%7B%22status%22%3Atrue%2C%22msg%22%3A%22%u83B7%u53D6%u6210%u529F%21%22%2C%22data%22%3A%7B%22username%22%3A%22139****5360%22%7D%7D',
        'sites_path': '/www/wwwroot',
        'site_model': 'php',
        'cna': '9dbada9446e64fa1b6f2090d2e4d7f61',
        '90f7209532efbcd84ed663aa163caf82': 'c1c3fff3-33b9-4824-8263-21b816815b45.mX0lNmarVxbII0leFX9GSkYcUSs',
        'request_token': '9fdJwkKivxBuTRi9zy7laSNB0B7pwpvCxMlQPiKLRddBWGZM',
        'backup_path': '/www/backup',
        'grafana_session': 'dc44db4a4a6bb890ac89d8e52e5f2b7a',
        'Hm_lvt_c35e3a563a06caee2524902c81975add': '1681093596,1682056131',
        'Hm_lpvt_c35e3a563a06caee2524902c81975add': '1682056131',
        'access_token': 'bearer%20eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MSwiZXhwIjoxNjgyMzAxMjQ4fQ.zyG8zME-JX--nc3GsaF6ioeiLsHQbsvtyt_bvnpt0w8',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7,und;q=0.6,ja;q=0.5',
        'Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MSwiZXhwIjoxNjgyMzAxMjQ4fQ.zyG8zME-JX--nc3GsaF6ioeiLsHQbsvtyt_bvnpt0w8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'order=id%20desc; serverType=nginx; pro_end=-1; ltd_end=-1; memSize=3931; bt_user_info=%7B%22status%22%3Atrue%2C%22msg%22%3A%22%u83B7%u53D6%u6210%u529F%21%22%2C%22data%22%3A%7B%22username%22%3A%22139****5360%22%7D%7D; sites_path=/www/wwwroot; site_model=php; cna=9dbada9446e64fa1b6f2090d2e4d7f61; 90f7209532efbcd84ed663aa163caf82=c1c3fff3-33b9-4824-8263-21b816815b45.mX0lNmarVxbII0leFX9GSkYcUSs; request_token=9fdJwkKivxBuTRi9zy7laSNB0B7pwpvCxMlQPiKLRddBWGZM; backup_path=/www/backup; grafana_session=dc44db4a4a6bb890ac89d8e52e5f2b7a; Hm_lvt_c35e3a563a06caee2524902c81975add=1681093596,1682056131; Hm_lpvt_c35e3a563a06caee2524902c81975add=1682056131; access_token=bearer%20eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MSwiZXhwIjoxNjgyMzAxMjQ4fQ.zyG8zME-JX--nc3GsaF6ioeiLsHQbsvtyt_bvnpt0w8',
        'Origin': 'http://api.cox.ink:8001',
        'Pragma': 'no-cache',
        'Referer': 'http://api.cox.ink:8001/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'X-Access-Token': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MSwiZXhwIjoxNjgyMzAxMjQ4fQ.zyG8zME-JX--nc3GsaF6ioeiLsHQbsvtyt_bvnpt0w8',
    }

    json_data = {
        'start_timestamp': 1681610049,
        'end_timestamp': 1682214849,
        'measurement': '测试任务',
        'retention_policy': 'default',
    }

    response = requests.post(
        'http://api.cox.ink:8001/feapder/monitor/get_points',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )

    # rjson = response.json()
    # pprint(rjson)

    rjson = {
        "type": 'line',
        "title": {
            "text": '最近几个月各品类销售趋势图'
        },
        "bgColor": '#fbfbfb',
        "labels": ['6月', '7月', '8月', '9月', '10月'],
        "datasets": [
            {
                "label": '家电',
                "data": [234, 278, 270, 190, 230]
            },
            {
                "label": '百货',
                "data": [164, 178, 150, 135, 160]
            },
            {
                "label": '食品',
                "data": [114, 138, 200, 235, 190]
            }
        ]
    }

    return rjson

def convert_log_record(log_record):
    # 转换浮点类型字段
    float_fields = ['created', 'msecs', 'relativeCreated']
    for field in float_fields:
        if field in log_record:
            log_record[field] = float(log_record[field])

    # 转换整数类型字段
    int_fields = ['lineno', 'levelno', 'process']
    for field in int_fields:
        if field in log_record:
            log_record[field] = int(log_record[field])

    # 转换元组类型字段
    tuple_fields = ['args', 'exc_info']
    for field in tuple_fields:
        if field in log_record:
            log_record[field] = eval(log_record[field])

    return log_record

from loguru import logger

@app.post("/log")
async def log_demo(request: Request):
    data = await request.body()
    fdata = await request.form()
    # 现在您可以使用 data 变量来访问请求发送来的数据
    log_data = data.decode("utf-8")
    # 将字节数据解码为字符串
    log_dict = parse_qs(log_data)

    # 将数据转换为字典
    # print(dict(fdata))
    # print(log_dict)

    # # 日志转换 logging
    # log_record = dict(fdata)
    # log_record = convert_log_record(log_record)
    # print(log_record)
    # log_record['asctime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(log_record['created']))
    #
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # formatted_log = formatter.format(logging.makeLogRecord(log_record))
    # print(f"这是叼毛输出的日志：{formatted_log}")

    # 日志转换 loguru
    log_record = dict(fdata)
    print(log_record)
    tmp = dict(fdata)
    message = log_record['msg']
    del tmp['levelname']
    del tmp['msg']
    logger.bind(**tmp).log(log_record['levelname'], message)
    vs = [v for k, v in tmp.items()]
    print(" | ".join(vs))
    return {"data": data}

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 8000
    uvicorn.run(app, host=HOST, port=PORT)
