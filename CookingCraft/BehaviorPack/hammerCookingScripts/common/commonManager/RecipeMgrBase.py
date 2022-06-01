'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-27 17:26:25
LastEditTime: 2022-04-27 17:32:52
'''

from abc import abstractmethod


class RecipeManagerBase(object):
    def __init__(self):
        object.__init__(self)

    @abstractmethod
    def GetResult(self, materials):
        """根据原料及配方获取生成物

        Args:
            materials (dict): 原材料字典
        """
        pass
