'''
Description: 设计模式工具
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-11 15:10:47
LastEditTime: 2022-07-27 15:19:11
'''


class Singleton(object):
    """单例设计模式，同于装饰类"""
    def __init__(self, cls):
        object.__init__(self)
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance(self._cls)
