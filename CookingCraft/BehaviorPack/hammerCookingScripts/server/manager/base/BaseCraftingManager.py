'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-26 19:15:11
LastEditTime: 2022-08-06 00:57:56
'''
from abc import abstractmethod
from copy import deepcopy

from hammerCookingScripts import logger
from hammerCookingScripts.server.manager.base.BaseWorkbenchManager import \
    BaseWorkbenchManager


class BaseCraftingManager(BaseWorkbenchManager):
    def __init__(self, blockName):
        BaseWorkbenchManager.__init__(self, blockName)

    def Tick(self):
        # type: () -> None
        """
        工作台没有动画需要 tick
        出于优化考虑，工作台合成物品由其他方法实现
        """
        return

    def CanSlotSet(self, *slotName):
        # type: (str) -> bool
        """判断槽位是否可以放置物品"""
        return all(
            isinstance(slot, int) or slot.startswith(self.materialSlotPrefix)
            for slot in slotName)

    def UpdateItemData(self, slotName, itemDict):
        # type: (str,dict) -> None
        """更新方块的物品数据"""
        self._ConvertToItemData(slotName, itemDict)

    def ConvertToSlotData(self):
        # type: () -> dict
        """将管理类的数据转换为 BlockEntityData 数据"""
        slotData = deepcopy(self.materialsItems)
        slotData.update(self.resultsItems)
        return slotData

    def Reset(self):
        # type: () -> dict
        """工作台重置，所有槽位返回原始状态，返回原材料操的所有物品作为掉落物"""
        self.materialsItems = {
            self.materialSlotPrefix + str(i): None
            for i in range(self.slotNum.get(self.materialSlotPrefix))
        }
        self.resultsItems = {
            self.resultSlotPrefix + str(i): None
            for i in range(self.slotNum.get(self.resultSlotPrefix))
        }

    def GetMaterialsItems(self):
        # type: () -> dict
        """获取原材料槽的物品字典"""
        return self.materialsItems

    def MatchRecipe(self):
        return self.proxy.MatchRecipe(self.materialsItems)

    def Produce(self):
        self._ConsumeMaterialsItems()
        self.resultsItems = {
            self.resultSlotPrefix + str(i): None
            for i in range(self.slotNum.get(self.resultSlotPrefix))
        }

    def GetAllSlotName(self):
        # type: () -> list
        """获取所有槽名，用于作为字典的键"""
        return self.materialsItems.keys() + self.resultsItems.keys()

    def _ConvertToItemData(self, slotName, itemDict):
        # type: (str,dict) -> None
        """更新方块的物品数据"""
        slotPrefix = self._GetSlotPrefix(slotName)
        if slotPrefix == self.materialSlotPrefix:
            self.materialsItems[slotName] = itemDict
        elif slotPrefix == self.resultSlotPrefix:
            self.resultsItems[slotName] = itemDict
        else:
            logger.error("不存在该槽位前缀名: {0}".format(slotPrefix))
            return
