#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/26
# CreatTIME : 18:04
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import redis
import uvicorn
from fastapi import FastAPI
from utils.RedisDBHelper import RedisDBHelper
from fastapi.middleware.cors import CORSMiddleware
from server_core.conf import redisconf
app = FastAPI()
rdb = RedisDBHelper(redisconf.db if redisconf.db else 0)
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/log")
async def log(data: str):
    rdb.set('log', data)
    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run("test02:app", host="0.0.0.0", port=8000)
