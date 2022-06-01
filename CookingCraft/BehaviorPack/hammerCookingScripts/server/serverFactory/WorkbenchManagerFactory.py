'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-28 14:00:50
LastEditTime: 2022-05-21 17:27:27
'''
from hammerCookingScripts.server.serverManager.CookingTableMgr import CookingTableManager
from hammerCookingScripts.server.serverManager.BakingFurnaceMgr import BakingFurnaceManager
from hammerCookingScripts.common import modConfig
from hammerCookingScripts import logger


class WorkbenchManagerFactory(object):
    """工作台管理工厂类，根据方块名返回不同的工作台管理类"""
    @classmethod
    def GetWorkbenchManager(cls, blockName):
        if blockName == modConfig.CookingTable_Block_Name:
            return CookingTableManager()
        elif blockName == modConfig.BakingFurnace_Block_Name:
            return BakingFurnaceManager()
        else:
            logger.error("没有 {0} 对应的管理类".format(blockName))
