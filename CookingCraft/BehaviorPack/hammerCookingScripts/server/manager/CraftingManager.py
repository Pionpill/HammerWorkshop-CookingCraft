'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-25 00:04:11
LastEditTime: 2022-08-25 00:06:01
'''

from hammerCookingScripts import logger
from hammerCookingScripts.server.manager.base import BaseCraftingManager
from hammerCookingScripts.common.utils import workbenchUtils


class CraftingManager(BaseCraftingManager):

    def __init__(self, blockName):
        BaseCraftingManager.__init__(self, blockName)

    def Reset(self):
        # type: () -> None
        """厨务台重置时，四个调料原材料槽(9-12)无需重置"""
        for i in range(
                workbenchUtils.GetFlexibleMaterialsSlotNum(self._blockName)):
            self.materialsItems[self.materialSlotPrefix + str(i)] = None
        self.resultsItems = {
            self.resultSlotPrefix + str(i): None
            for i in range(self.slotNum.get(self.resultSlotPrefix))
        }

    def GetMaterialsItems(self, part=False):
        # type: (bool) -> dict
        """part 设置为 True 可仅获取非调料槽和碗槽的物品"""
        if not part:
            return super().GetMaterialsItems()
        itemDict = {}
        for i in range(
                workbenchUtils.GetFlexibleMaterialsSlotNum(self._blockName)):
            key = self.materialSlotPrefix + str(i)
            itemDict[key] = self.materialsItems.get(key)
        return itemDict
