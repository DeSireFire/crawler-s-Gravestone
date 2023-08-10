#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/28
# CreatTIME : 14:09
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'


from logClient import CrawlLogUper
obj = CrawlLogUper(
    token="a158dc3a9d0f71283132f2c1127bc8c0",
    uper_name="tester",
    up_switch=False
)
#
logger = obj.logger

# 根据需要，在你想的代码位置加入日志打印
logger.info(f'这是一条 信息 日志，发出来测试一下！！！')
logger.warning(f'这是一条 警告 日志，发出来测试一下！！！')
logger.error(f'这是一条 错误 日志，发出来测试一下！！！')

logger.debug(f'这是一条 调试 日志，发出来测试一下！！！')

# 如果需要推送数据入库计数
# obj.items_total()

# 如果程序运行完或者需要手动关闭推送任务
# end_point()