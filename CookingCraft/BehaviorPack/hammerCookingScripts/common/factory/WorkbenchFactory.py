'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-23 18:00:11
LastEditTime: 2022-07-27 15:26:20
'''
from hammerCookingScripts import logger
from hammerCookingScripts.common.proxy import (BakingFurnaceRecipeProxy,
                                               CookingTableRecipeProxy)


class WorkbenchFactory(object):
    proxyDict = {}

    @classmethod
    def GetWorkbenchProxy(cls, blockName):
        # type: (str) -> BakingFurnaceRecipeProxy
        """
        获取工作台代理类
        单例模式，仅提供一个实例
        """
        if cls.proxyDict.get(blockName):
            return cls.proxyDict.get(blockName)

        if blockName == "cookingcraft:cooking_table":
            cls.proxyDict[blockName] = CookingTableRecipeProxy()
        elif blockName == "cookingcraft:baking_furnace":
            cls.proxyDict[blockName] = BakingFurnaceRecipeProxy()
        else:
            logger.warn("没有 {0} 对应的代理类".format(blockName))
            return

        return cls.proxyDict.get(blockName)
