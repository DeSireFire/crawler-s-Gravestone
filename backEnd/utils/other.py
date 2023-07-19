#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/7/19
# CreatTIME : 11:38
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'


def get_md5(s):
    """
    字符串转md5
    :param s:
    :return:
    """
    import hashlib
    m = hashlib.md5(s.encode())
    res = m.hexdigest()
    return res