'''
Description: 路径包
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-02 17:04:37
LastEditTime: 2022-08-02 17:35:05
'''


def JoinPath(*args):
    # type: (str) -> str
    """将多个路径用 '/' 连接"""
    path = ""
    for arg in args:
        path = arg if path == "" else "{0}/{1}".format(path, arg)
    return path


def GetSupPath(path):
    # type: (str) -> str
    """获取上一级路径"""
    pos = path.rfind("/")
    return path[:pos]
