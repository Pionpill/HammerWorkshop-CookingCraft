'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-23 18:00:11
LastEditTime: 2022-08-11 16:31:45
'''
from hammerCookingScripts import logger
from hammerCookingScripts.common.proxy import (BakingFurnaceRecipeProxy,
                                               CookingTableRecipeProxy,
                                               MillRecipeProxy)


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
        elif blockName == "cookingcraft:mill":
            cls.proxyDict[blockName] = MillRecipeProxy()
        else:
            logger.warn("没有 {0} 对应的代理类".format(blockName))
            return

        return cls.proxyDict.get(blockName)
