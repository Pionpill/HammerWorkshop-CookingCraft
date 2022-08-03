'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-27 15:53:27
LastEditTime: 2022-07-30 15:34:20
'''
from hammerCookingScripts import logger
from hammerCookingScripts.common.utils import workbenchUtils
from hammerCookingScripts.server.manager import CraftingManager
from hammerCookingScripts.server.manager import FurnaceManager


class WorkbenchFactory(object):
    managerDict = {}

    @classmethod
    def GetWorkbenchManager(cls, exaPos, blockName=None):
        # type: (tuple,str) -> FurnaceManager
        """
        获取工作台管理类
        若不存在对应的管理类则自动创建
        exaPos: (x,y,z,dimensionId)
        """
        if cls.managerDict.get(exaPos):
            return cls.managerDict.get(exaPos)
        if not blockName:
            logger.info("缺少 blockName, 无法创建新的管理类")
            return
        if workbenchUtils.IsFurnaceBlock(blockName):
            cls.managerDict[exaPos] = FurnaceManager(blockName)
        elif workbenchUtils.IsCraftingBlock(blockName):
            cls.managerDict[exaPos] = CraftingManager(blockName)
        else:
            logger.debug("{0} 无法找到对应的管理类".format(blockName))
            return
        return cls.managerDict.get(exaPos)

    @classmethod
    def DestroyWorkbenchManager(cls, exaPos):
        # type: (tuple) -> None
        """
        删除工作台管理类
        exaPos: (x,y,z,dimensionId)
        """
        if cls.managerDict.get(exaPos):
            del cls.managerDict[exaPos]
        else:
            logger.info("{0} 处无法销毁模组工作台管理类".format(exaPos))
            return
