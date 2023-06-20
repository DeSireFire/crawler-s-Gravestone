#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/29
# CreatTIME : 17:36
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
# 初始化
import os

# 封装等级(低到高)
# auth、model <= views <= (users)init

# 导入视图
from .views import *

# 检查并创建业务日志文件夹
path = os.path.join(BASE_DIR, "logs", "worker_logs")
if not os.path.exists(path):
    os.makedirs(path)

