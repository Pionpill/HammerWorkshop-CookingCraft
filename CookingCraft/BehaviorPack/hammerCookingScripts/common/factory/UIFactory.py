'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-31 14:01:04
LastEditTime: 2022-08-04 14:52:51
'''
from hammerCookingScripts.common.proxy import UIProxy


class UIFactory(object):
    proxy = UIProxy()

    @classmethod
    def GetUIProxy(cls):
        """返回 UI 代理类，采用单例设计模式"""
        return cls.proxy
