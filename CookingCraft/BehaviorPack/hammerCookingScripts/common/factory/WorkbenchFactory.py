'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-23 18:00:11
LastEditTime: 2022-08-24 22:28:12
'''
from hammerCookingScripts import logger
from hammerCookingScripts.common.proxy import CraftingRecipeProxy, FurnaceRecipeProxy
from hammerCookingScripts.common.utils import workbenchUtils


class WorkbenchFactory(object):
    proxyDict = {}

    @classmethod
    def GetWorkbenchProxy(cls, blockName):
        # type: (str) -> FurnaceRecipeProxy
        """
        获取工作台代理类
        单例模式，仅提供一个实例
        """
        if cls.proxyDict.get(blockName):
            return cls.proxyDict.get(blockName)
        if workbenchUtils.IsCraftingBlock(blockName):
            cls.proxyDict[blockName] = CraftingRecipeProxy(blockName)
        elif workbenchUtils.IsFurnaceBlock(blockName):
            cls.proxyDict[blockName] = FurnaceRecipeProxy(blockName)
        else:
            logger.warn("没有 {0} 对应的代理类".format(blockName))
            return

        return cls.proxyDict.get(blockName)
